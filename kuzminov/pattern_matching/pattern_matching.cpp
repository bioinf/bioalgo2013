// KnuthRabinKarp.cpp : Defines the entry point for the console application.
//

#include <iostream>
#include <fstream>
#include <string>
#include <vector>

using namespace std;

std::ifstream fsIn("input.txt");
std::ofstream fsOut("output.txt");

struct FASTA
{
  struct Item
  {
    string Name;
    string Sequence;
  };
  vector<Item> Items;
};

void ReadFASTA( FASTA &fasta )
{
  string s;
  while(!cin.eof())
  {
    getline(std::cin, s);
    if(s[0] == '>')
    {
      FASTA::Item item;
      item.Name = s.substr(1);

      fasta.Items.push_back(item);
    }
    else
    {
      fasta.Items.back().Sequence += s;
    }
  }
}

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

void GenerateRandomData(string &text, string &sample)
{
  int text_len = 100, sample_len = 5;
  text.resize(text_len);
  sample.resize(sample_len);
  for(int i=0; i<text_len; ++i)
  {
    text[i] = RandomSymbol();
  }
  for(int i=0; i<sample_len; ++i)
  {
    sample[i] = RandomSymbol();
  }
}

int BruteForce(const string &text, const string &sample)
{
  for(int i=0; i<text.size() - sample.size() + 1; ++i)
  {
    for(int j=0; ; ++j)
    {
      if(j == sample.size())
      {
        return i;
      }
      if(text[i + j] != sample[j])
      {
        break;
      }
    }
  }
  return -1;
}

int KMP_prefix(const string &text, const string &sample)
{
  vector<int> prefix(sample.size(), 0);

  int prev = 0;
  for(int k=1; k<sample.size(); ++k)
  {
    for(int l=1; l<= prev+1; ++l)
    {
      string s1 = sample.substr(0,l);
      string s2 = sample.substr(k-l+1,l);
      if(s1 == s2)
          prefix[k] = l;
    }
    prev = prefix[k];
  }

  for(int i=0, j=0; i<text.size() - sample.size() + 1; )
  {
    if(j == sample.size())
    {
      return i;
    }
    if(text[i + j] == sample[j])
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
        //sample[0, j-1] == text[i, i+j-1]
        if(prefix[j-1] != 0)
        {
          i += j - prefix[j-1];
          j = prefix[j-1];
        }
        else
        {
          ++i;
          j=0;
        }
      }
    }
  }

  return -1;
}

int Z_function(const string &text, const string &sample)
{
  vector<int> Z(sample.size() + 1 + text.size(), 0);
  for(int i=1; i<Z.size(); ++i)
  {
    Z[i] = 0;
  }
  Z[0] = Z.size();

  string str = sample + "$" + text;

  for( int curr = 1, left = 0, right = 1; curr < Z.size(); ++curr )
  {
    if( curr >= right )
    {
      int off = 0;
      while( curr + off < Z.size() && str[curr + off] == str[off] )
          ++off;
      Z[curr] = off;
      if(Z[curr] == sample.size())
          return curr - sample.size() - 1;
      right = curr + Z[curr];
      left = curr;
    }
    else
    {
      const size_t equiv = curr - left;
      if( Z[equiv] < right - curr )
      {
        Z[curr] = Z[equiv];
      }
      else
      {
        size_t off = 0;
        while( right + off < Z.size() && str[right - curr + off] == str[right + off] )
            ++off;
        Z[curr] = right - curr + off;
        right += off;
        left = curr;
      }
    }
  }




  return -1;
}

int RabinKarp(const string &text, const string &sample)
{
  int h = 0;
  static int m[256];
  m['A'] = 0; m['C'] = 1; m['G'] = 2; m['T'] = 3;
  const int p = 524287;
  const int d = 4;

  if(text.size() < sample.size())
      return -1;

  int h1 = 0;
  int D = 1;
  for(int i=sample.size()-1; i>=0; --i)
  {
    h = (h*d + m[sample[i]]) % p;
    h1 = (h1*d + m[text[i]]) % p;
    D = D*d % p;
  }

  if(h == h1)
  {
    //check...
    return 0;
  }

  for(int i=sample.size(); i<text.size(); ++i)
  {
    h1 /= d;
    h1 = (h1 + m[text[i]]*D/d) % p;
    if(h == h1)
    {
      //check...
      return i - sample.size() + 1;
    }
  }

  return -1;
}

bool Check(const string &text, const string &sample, int pos)
{
  if(pos == -1)
  {
    return text.find(sample) == string::npos;
  }
  return text.substr(pos, sample.size()) == sample;   
}


int main(int argc, char* argv[])
{
  if(!fsIn.is_open())
  {
    std::cout << "No input file found";
  }
  std::cin.rdbuf( fsIn.rdbuf() );

  for(int i=0; i<1000; ++i)
  {
    string text, sample;

    GenerateRandomData(text, sample);
    int i1 = BruteForce(text, sample);
    int i2 = KMP_prefix(text, sample);
    int i3 = Z_function(text, sample);
    int i4 = RabinKarp(text, sample);
    if(i1 != i2 || i2 != i3 || i3 != i4)
    {
      cout << "error: different results" << endl;
      break;
    }
    else
    {
      cout << i << " success, " << i1 << endl;
    }
    if(!Check(text, sample, i1))
    {
      cout << "error: template doesn't match" << endl;
      break;
    }
  }



/*  vector<int> result(dna.size(), 0);

  int prev = 0;
  for(int k=1; k<dna.size(); ++k)
  {
    for(int l=1; l<= prev+1; ++l)
    {
      string s1 = dna.substr(0,l);
      string s2 = dna.substr(k-l+1,l);
      if(s1 == s2)
          result[k] = l;
    }
    prev = result[k];
  }

  for(vector<int>::iterator iter = result.begin(); iter != result.end(); ++iter)
  {
    cout << *iter << " ";
    fsOut << *iter << " ";
  }*/

	return 0;
}

