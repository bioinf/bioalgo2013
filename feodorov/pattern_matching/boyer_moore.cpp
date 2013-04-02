#include "algorithms.h"
#include "utils.h"

std::vector<int>& get_failure_array(std::string& pattern, std::vector<int>& failure_array);

void boyer_moor_bad_char_preprocess(const std::string& pattern, std::map<char, std::list<int> >& res)
{
	for(int i = (int)pattern.length() - 1; i >= 0; --i)
	{
		res[pattern[i]].push_back(i);
	}
}

int boyer_moor_get_nearest_left_same_char_pos(const std::map<char, std::list<int> >& data, char c, int pos)
{
	std::map<char, std::list<int> >::const_iterator it;
	if(data.end() != (it = data.find(c)))
	{
		for(std::list<int>::const_iterator iter = it->second.begin(); iter != it->second.end(); ++iter)
		{
			if(*iter < pos)
			{
				return *iter;
			}
		}
	}

	return -1;
}

std::vector<int>& boyer_moor_bad_char(std::string& text, std::string& pattern, std::vector<int>& res)
{
	std::map<char, std::list<int> > data;
	boyer_moor_bad_char_preprocess(pattern, data);
//	print_map_of_lists(data);

	int i = pattern.length() - 1;

	while(i < (int)text.length())
	{
		int k = 0;
		//iterate through pattern to find matches
		for(; k < (int)pattern.length(); ++k)
		{
			//if mismatch - shift right by bad-char-table-rule
			if(text[i - k] != pattern[pattern.length() - 1 - k])
			{
				char char_to_found = text[i - k];
				int from_pos = pattern.length() - 1 - k;
				int pos = boyer_moor_get_nearest_left_same_char_pos(data, char_to_found, from_pos);
				i += pos == -1 ? 1 : from_pos - pos;
				break;
			}
		}

		if(k == (int)pattern.length())
		{
			res.push_back(i - k + 1);
			i++;
		}
	}

	return res;
}

void boyer_moore_suffixes(const std::string& pattern, std::vector<int>& suffix)
{
   int f, g, i, m = pattern.length();
   suffix[m - 1] = m;

   g = m - 1;
   for (i = m - 2; i >= 0; --i)
   {
      if (i > g && suffix[i + m - 1 - f] < i - g)
      {
    	  suffix[i] = suffix[i + m - 1 - f];
      }
      else
      {
         if (i < g)
         {
            g = i;
         }
         f = i;
         while (g >= 0 && pattern[g] == pattern[g + m - 1 - f])
         {
            --g;
         }
         suffix[i] = f - g;
      }
   }
}

void boyer_moor_good_suffixes_preprocess(const std::string& pattern, std::vector<int>& goodSuffixes)
{
   int i, j = 0, m = pattern.length();
   std::vector<int> suff(m);
   boyer_moore_suffixes(pattern, suff);

   for (i = m - 1; i >= 0; --i)
   {
      if (suff[i] == i + 1)
      {
         for (; j < m - 1 - i; ++j)
         {
            if (goodSuffixes[j] == m)
            {
            	goodSuffixes[j] = m - 1 - i;
            }
         }
      }
   }

   for (i = 0; i <= m - 2; ++i)
   {
	   goodSuffixes[m - 1 - suff[i]] = m - 1 - i;
   }
}

std::vector<int>& boyer_moor_good_suffix(std::string& sequence, std::string& pattern, std::vector<int>& res)
{
	int i, j = 0;
	std::vector<int> suffix(pattern.length(), pattern.length());
	boyer_moor_good_suffixes_preprocess(pattern, suffix);

	while (j <= (int)sequence.length() - (int)pattern.length())
	{
      for (i = pattern.length() - 1; i >= 0 && pattern[i] == sequence[i + j]; --i);

      if (i < 0)
      {
         res.push_back(j);
         j += suffix[0];
      }
      else
      {
         j += suffix[i];
      }
   }

	return res;
}

std::vector<int>& boyer_moor_galil(std::string& sequence, std::string& pattern, std::vector<int>& res)
{
	int i, j = 0;
	std::vector<int> suffix(pattern.length(), pattern.length());
	boyer_moor_good_suffixes_preprocess(pattern, suffix);

	std::vector<int> failure;
	failure = get_failure_array(pattern, failure);
	int l = failure.back();

	while (j <= (int)sequence.length() - (int)pattern.length())
	{
		//http://orion.lcg.ufrj.br/Dr.Dobbs/books/book5/chap10.htm
		//comparison not includes prefix that is suffix
		for (i = pattern.length() - 1; i >= l - 1 && pattern[i] == sequence[i + j]; --i);

		if (i < 0)
		{
			res.push_back(j);
			j += suffix[0];
		}
		else
		{
			j += suffix[i];
		}
   }

	return res;
}
