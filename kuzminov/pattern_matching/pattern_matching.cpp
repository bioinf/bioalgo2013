// KnuthRabinKarp.cpp : Defines the entry point for the console application.
//

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <sstream>
#include <time.h>

using namespace std;

std::ifstream fsIn("input.txt");
std::ofstream fsOut("output.txt");

static int m[256];

char RandomSymbol()
{
  int r = rand();
  switch(r%4)
  {
  case 0:
    return 'A';
  case 1:
    return 'C';
  case 2:
    return 'G';
  case 3:
    return 'T';
  }
}

void GenerateRandomData(string &haystack, string &needle, int haystack_len = 100, int needle_len = 5)
{
  haystack.resize(haystack_len);
  needle.resize(needle_len);
  for(int i=0; i<haystack_len; ++i)
  {
    haystack[i] = RandomSymbol();
  }
  for(int i=0; i<needle_len; ++i)
  {
    needle[i] = RandomSymbol();
  }
}


class MatchVisitor
{
public:
  virtual void Visit(const string &haystack, const string &needle, int position) = 0;
  virtual void Finished(const string &haystack, const string &needle) = 0;
};

class DummyMatchVisitor: public MatchVisitor
{
public:
  void Visit(const string &haystack, const string &needle, int position) {}
  void Finished(const string &haystack, const string &needle) {}
};

class PrinterMatchVisitor: public MatchVisitor
{
private:
  int Count;
public:
  PrinterMatchVisitor() : Count(0) {}
  void Visit(const string &haystack, const string &needle, int position)
  {
    cout << haystack << endl;
    for(int i = 0; i < position; ++i)
    {
      cout << " ";
    }
    cout << needle << endl;
    ++Count;
  }
  void Finished(const string &haystack, const string &needle)
  {
    cout << "Finished searching, " << Count << " matches found." << endl;
  }
};

class VerifierMatchVisitor: public MatchVisitor
{
private:
  vector<int> Matches;
public:
  void Visit(const string &haystack, const string &needle, int position)
  {
    if( position < 0 || position > haystack.size() - needle.size() )
    {
      cout << "Error: invalid range. position == " << position;
    }
    if( haystack.substr(position, needle.size()) != needle )
    {
      cout << "Error: invalid match\n";
      PrinterMatchVisitor printer;
      printer.Visit(haystack, needle, position);
    }
    Matches.push_back(position);
  }
  void Finished(const string &haystack, const string &needle)
  {
  }
  bool operator == (const VerifierMatchVisitor &verifier)
  {
    // Assuming that the vectors are sorted
    if(Matches.size() != verifier.Matches.size())
        return false;
    for(int i=0; i<Matches.size(); ++i)
    {
      if(Matches[i] != verifier.Matches[i])
          return false;
    }
    return true;
  }
  bool operator != (const VerifierMatchVisitor &verifier)
  {
    return !operator == (verifier);
  }
};


void BruteForce(const string &haystack, const string &needle, MatchVisitor &visitor)
{
  for(int i=0, count = haystack.size() - needle.size() + 1; i<count; ++i)
  {
    for(int j=0; ; ++j)
    {
      if(j == needle.size())
      {
        visitor.Visit(haystack, needle, i);
        break;
      }
      if(haystack[i + j] != needle[j])
      {
        break;
      }
    }
  }
  visitor.Finished(haystack, needle);
}

void KMP_prefix(const string &haystack, const string &needle, MatchVisitor &visitor)
{
  vector<int> prefix(needle.size(), 0);

  int k = 0;
  for(int i = 1; i < needle.size(); ++i)
  {          
    while( (k > 0) && (needle[k] != needle[i]) ) 
        k = prefix[k-1]; 
    if (needle[k] == needle[i])
        k++;
    prefix[i] = k;
  }

  for(int i=0, j=0, count=(haystack.size() - needle.size() + 1); i < count; )
  {
    if(j == needle.size())
    {
      visitor.Visit(haystack, needle, i);
      ++i;
      j=0;
    }
    if(haystack[i + j] == needle[j])
    {
      ++j;
    }
    else
    {
      if(j == 0)
      {
        ++i;
      }
      else
      {
        //note: needle[0, j-1] == haystack[i, i+j-1]
        int p = prefix[j-1];
        if(p != 0)
        {
          i += j - p;
          j = p;
        }
        else
        {
          ++i;
          j=0;
        }
      }
    }
  }

  visitor.Finished(haystack, needle);
}

void Z_function(const string &haystack, const string &needle, MatchVisitor &visitor)
{
  vector<int> Z(needle.size() + 1 + haystack.size(), 0);
  Z[0] = Z.size();

  string str = needle + "$" + haystack;

  for( int curr = 1, left = 0, right = 0, j = 0; curr < Z.size(); ++curr )
  {
    if( curr > right )
    {
      for(j = 0; ((j + curr) < Z.size()) && (str[curr + j] == str[j]) ; ++j);
      Z[curr] = j;
      left = curr;
      right = curr + j - 1;
    }
    else
    {
      if(curr + Z[curr - left] < right + 1)
          Z[curr] = Z[curr - left];
      else
      {
        for(j = 1; (str[right + j] == str[right - curr + j]) && ((j + right) < Z.size()); ++j);
        Z[curr] = right - curr + j;
        left = curr;
        right += j - 1;
      }
    }

    if(Z[curr] == needle.size())
    {
      visitor.Visit(haystack, needle, curr - needle.size() - 1);
    }
  }

  visitor.Finished(haystack, needle);
}

void RabinKarp_NoChecks(const string &haystack, const string &needle, MatchVisitor &visitor)
{
  int h = 0;
  const int p = 401;//524287;
  const int d = 4;

  if(haystack.size() >= needle.size())
  {
    int h1 = 0;
    int D = 1;
    for(int i=0; i<needle.size(); ++i)
    {
      h = (h*d + m[needle[i]]) % p;
      h1 = (h1*d + m[haystack[i]]) % p;
      D = D*d % p;
    }

    if(h == h1)
    {
      visitor.Visit(haystack, needle, 0);
    }

    for(int ii=needle.size(); ii<haystack.size(); ++ii)
    {
      h1 *= d;
      h1 -= D * m[haystack[ii-needle.size()]];
      if(h1 < 0)
        h1 += p;
      h1 += m[haystack[ii]];
      h1 %= p;
      if(h == h1)
      {
        visitor.Visit(haystack, needle, ii - needle.size() + 1);
      }
    }
  }

  visitor.Finished(haystack, needle);
} 

void RabinKarp_WithChecks(const string &haystack, const string &needle, MatchVisitor &visitor)
{
  class CheckDecoratorMatchVisitor: public MatchVisitor
  {
  private:
    MatchVisitor &DecoratedVisitor;

    void Visit(const string &haystack, const string &needle, int position)
    {
      // Assuming that the position is valid
      if( haystack.substr(position, needle.size()) == needle )
      {
        DecoratedVisitor.Visit(haystack, needle, position);
      }
    }
    void Finished(const string &haystack, const string &needle)
    {
      DecoratedVisitor.Finished(haystack, needle);
    }
  public:
    CheckDecoratorMatchVisitor(MatchVisitor &decoratedVisitor) : DecoratedVisitor(decoratedVisitor) {}
  };

  RabinKarp_NoChecks(haystack, needle, CheckDecoratorMatchVisitor(visitor));
} 

void BoyerMoore_StopSymbol(const string &haystack, const string &needle, MatchVisitor &visitor)
{
  int STOP[4] = {0, 0, 0, 0};
  for(int i = needle.size() - 2; i >= 0; --i)
  {
    int ind = m[needle[i]];
    STOP[ind] = max(STOP[ind], i+1);
  }


  for(int i=0; i<haystack.size() - needle.size() + 1; ++i)
  {
    for(int j=needle.size() - 1; ; --j)
    {
      if(j < 0)
      {
        visitor.Visit(haystack, needle, i);
        break;
      }
      if(haystack[i + j] != needle[j])
      {
        if(j == needle.size() - 1)
        {
          int stop_symbol = STOP[m[haystack[i+j]]];
          int stop_symbol_additional = j - (stop_symbol != 0 ? stop_symbol : 0);
          i += stop_symbol_additional;
        }
        else
        {
          
        }
        break;
      }
    }
  }
  visitor.Finished(haystack, needle);
}

void BoyerMoore_Suffix(const string &haystack, const string &needle, MatchVisitor &visitor)
{
  int STOP[4] = {0, 0, 0, 0};
  for(int i = needle.size() - 2; i >= 0; --i)
  {
    int ind = m[needle[i]];
    STOP[ind] = max(STOP[ind], i+1);
  }


  vector<int> prefix(needle.size(), 0);
  int k = 0;
  for(int i = 1; i < needle.size(); ++i)
  {          
    while( (k > 0) && (needle[k] != needle[i]) ) 
        k = prefix[k-1]; 
    if (needle[k] == needle[i])
        k++;
    prefix[i] = k;
  }

  string needle1; needle1.resize(needle.size());
  for(int i=0; i<needle.size(); ++i)
  {
    needle1[i] = needle[needle.size() - i - 1];
  }
  vector<int> prefix1(needle1.size(), 0);
  k = 0;
  for(int i = 1; i < needle.size(); ++i)
  {          
    while( (k > 0) && (needle1[k] != needle1[i]) ) 
        k = prefix[k-1]; 
    if (needle1[k] == needle1[i])
        k++;
    prefix1[i] = k;
  }

  vector<int> suffshift(needle.size()+1);
  for(int j = 0; j<needle.size(); ++j)
  {
    suffshift[j] = needle.size() - prefix[j];
  }
  for(int i = 1; i<needle.size(); ++i)
  {
    int j = needle.size() - prefix1[i];
    suffshift[j] = min(suffshift[j], i - prefix1[i]);
  }


  vector<int> suffics_table(needle.size()+1);
  for(int i = 0; i <= needle.length(); ++i)
  {
    suffics_table[i] = needle.length() - prefix.back();
  }
  for(int i = 1; i < needle.length(); ++i)
  {
    int j = prefix1[i];
    suffics_table[j] = min(suffics_table[j], i - prefix1[i] + 1);
  }



  for(int i=0; i<haystack.size() - needle.size() + 1; ++i)
  {
    for(int j=needle.size() - 1; ; --j)
    {
      if(j < 0)
      {
        visitor.Visit(haystack, needle, i);
        break;
      }
      if(haystack[i + j] != needle[j])
      {
        if(j == needle.size() - 1)
        {
          int stop_symbol = STOP[m[haystack[i+j]]];
          int stop_symbol_additional = j - (stop_symbol != 0 ? stop_symbol : 0);
          i += stop_symbol_additional;
        }
        else
        {
          i += suffics_table[needle.length() - j - 1] - 1;      
        }
        break;
      }
    }
  }
  visitor.Finished(haystack, needle);
}


class TTimer
{
public:
  typedef void (*TimerFunc)( long mSec );
private:
  clock_t StartedAt;
  TimerFunc Func;
public:
  TTimer( TimerFunc f )
    : Func(f)
  {
    StartedAt = clock();
  }
  ~TTimer()
  {
    Func( (clock() - StartedAt) / (CLOCKS_PER_SEC/1000) );
  }
};

void PrintMSec( long mSec )
{
  cout << mSec << " msec" << endl;
}

void CompeteSample(const string &title, const string &haystack, const string &needle, int num)
{
  VerifierMatchVisitor verifier1;
  VerifierMatchVisitor verifier2;
  VerifierMatchVisitor verifier3;
  VerifierMatchVisitor verifier4;
  VerifierMatchVisitor verifier5;
  VerifierMatchVisitor verifier6;
  BruteForce(haystack, needle, verifier1);
  KMP_prefix(haystack, needle, verifier2);
  Z_function(haystack, needle, verifier3);
  RabinKarp_WithChecks(haystack, needle, verifier4);
  BoyerMoore_StopSymbol(haystack, needle, verifier5);
  BoyerMoore_Suffix(haystack, needle, verifier6);
  if(verifier1 != verifier2 || verifier2 != verifier3 || verifier3 != verifier4 || verifier4 != verifier5 || verifier5 != verifier6)
  {
    cout << "Ooopps!" << endl;
    return;
  }

  cout << "\t" << title << endl;
  //cout << "haystack == " << haystack << endl;
  //cout << "needle == " << needle << endl;


  {
    cout << "Brute Force: \t\t\t";
    TTimer timer(PrintMSec);
    for(int j = 0; j<num; ++j)
    {
      DummyMatchVisitor dummy;
      BruteForce(haystack, needle, dummy);
    }
  }
  {
    cout << "KMP: \t\t\t\t";
    TTimer timer(PrintMSec);
    for(int j = 0; j<num; ++j)
    {
      DummyMatchVisitor dummy;
      KMP_prefix(haystack, needle, dummy);
    }
  }
  {
    cout << "Z-function: \t\t\t";
    TTimer timer(PrintMSec);
    for(int j = 0; j<num; ++j)
    {
      DummyMatchVisitor dummy;
      Z_function(haystack, needle, dummy);
    }
  }
/*  {
    cout << "Rabin-Karp, no checks: \t\t";
    TTimer timer(PrintMSec);
    for(int j = 0; j<num; ++j)
    {
      DummyMatchVisitor dummy;
      RabinKarp_NoChecks(haystack, needle, dummy);
    }
  }*/
  {
    cout << "Rabin-Karp, with checks: \t";
    TTimer timer(PrintMSec);
    for(int j = 0; j<num; ++j)
    {
      DummyMatchVisitor dummy;
      RabinKarp_WithChecks(haystack, needle, dummy);
    }
  }
  {
    cout << "Boyer-Moore, Stop symbol: \t";
    TTimer timer(PrintMSec);
    for(int j = 0; j<num; ++j)
    {
      DummyMatchVisitor dummy;
      BoyerMoore_StopSymbol(haystack, needle, dummy);
    }
  }
  {
    cout << "Boyer-Moore, Suffix: \t\t";
    TTimer timer(PrintMSec);
    for(int j = 0; j<num; ++j)
    {
      DummyMatchVisitor dummy;
      BoyerMoore_Suffix(haystack, needle, dummy);
    }
  }
  cout << endl;
}

int main(int argc, char* argv[])
{
  if(!fsIn.is_open())
  {
    std::cout << "No input file found";
  }
  std::cin.rdbuf( fsIn.rdbuf() );

  // Prepare for Rabin-Karp and Boyer-Moore:
  m['A'] = 0; m['C'] = 1; m['G'] = 2; m['T'] = 3;

  CompeteSample("Brute Force benefit",
                "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
                "CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC",
                100000);
  CompeteSample("KMP benefit",
                "AAAAAAAAAAAAAAAAAAAAAAACAAAAAAAAAAAAAAAAAAAAAAACAAAAAAAAAAAAAAAAAAAAAAACAAAAAAAAAAAAAAAAAAAAAAAC",
                "AAAAAAAAAAAAAAAAAAAAAAAC",
                100000);
  CompeteSample("Rabin-Karp benefit",
                "ATCGGAGTCGAGATCGGAGTCGAGATCGGAGTCGAGATCGGAGTCGAGATCGGAGTCGAGATCGGAGTCGAGATCGGAGTCGAGATCGGAGTCGAG",
                "ATCGGAGTCGAGT",
                100000);

  for(int i=0; i<100; ++i)
  {
    string haystack, needle;

    GenerateRandomData(haystack, needle, 10000, 20);                                                                                                                                                    //

    //BruteForce(haystack, needle, PrinterMatchVisitor());
    //KMP_prefix(haystack, needle, PrinterMatchVisitor());
    //Z_function(haystack, needle, PrinterMatchVisitor());
    //RabinKarp_WithChecks(haystack, needle, PrinterMatchVisitor());
    //BoyerMoore_StopSymbol(haystack, needle, PrinterMatchVisitor());
    //BoyerMoore_Suffix(haystack, needle, PrinterMatchVisitor());

    stringstream ss;
    ss << string("Random test ") << i;
    CompeteSample(ss.str(), haystack, needle, 1000);
  }

  for(;;);
	return 0;
}

