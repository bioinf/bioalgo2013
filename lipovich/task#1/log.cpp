#include "log.h"

extern std::ofstream ofs;

void log_res(const std::string alg, const std::string& p, const std::string& t, double time, TResult& res)
{
    ofs << alg << " method:" << std::endl << std::endl;

    if (t.length() <= max_disp_length)
    {
        ofs << p << std::endl << t << std::endl;
    }
    else
    {
        ofs << "Text too long for display..." << std::endl;
    }

    ofs << std::endl << "Pattern matching positions in text:" << std::endl;

    for (int i = 0; i < res.size(); ++i)
    {
        ofs << res[i] << " ";
    }

    ofs.precision(5);

    ofs << std::endl << "Computation time: " << time << std::endl << std::endl;


    ofs << std::endl << std::endl;
}
