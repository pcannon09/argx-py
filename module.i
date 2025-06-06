%module argx_py
%{
#include "../tmp/argx/inc/types.hpp"
#include "../tmp/argx/inc/macros.hpp"
#include "../tmp/argx/inc/ARGXAddError.hpp"
#include "../tmp/argx/inc/Argx.hpp"
using namespace argx;
%}

%include "std_string.i"
%include "std_vector.i"

// Template instantiations for STL containers you use explicitly:
namespace std {
    %template(StringVector) vector<string>;
    %template(ARGXOptionsVector) vector<argx::ARGXOptions>;
}

// Make sure ARGXOptions destructor is visible
%include "./tmp/argx/inc/types.hpp"
%include "./tmp/argx/inc/macros.hpp"
%include "./tmp/argx/inc/ARGXAddError.hpp"

// Ignore default Argx constructor if not needed:
%ignore Argx::Argx();

// Extend Argx with Python-friendly constructor wrapping:
%extend argx::Argx {
    Argx(const std::string &id, const std::vector<std::string> &args) {
        // Copy args to avoid lifetime issues with references
        std::vector<std::string> temp_args = args;
        return new Argx(id, temp_args);
    }
}

// Finally include Argx.hpp to wrap Argx class:
%include "./tmp/argx/inc/Argx.hpp"

%inline %{
void addSubParam(argx::ARGXOptions &opt, const argx::ARGXOptions &sub) {
    opt.subParams.push_back(sub);
}
%}
