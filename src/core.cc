#include <boost/python.hpp>
#include <boost/optional/optional.hpp>

#include <nix.hpp>
#include <transmorgify.hpp>
#include <accessors.hpp>

#include <PyEntity.hpp>

using namespace boost::python;
using namespace nix;
using namespace base;
using namespace nixpy;




BOOST_PYTHON_MODULE(core)
{
    // set options for doc strings
    // show user defined / show py signatures / don't show cpp signatures
    docstring_options local_docstring_options(true, true, false);

    PyFile::do_export();

    PySection::do_export();
    PyProperty::do_export();
    PyValue::do_export();

    PyBlock::do_export();
    PySource::do_export();
    PyDataArray::do_export();
    PyDimensions::do_export();
    PyFeature::do_export();
    PySimpleTag::do_export();
    PyDataTag::do_export();

    to_python_converter<boost::optional<std::string>, option_transmogrify<std::string>>();
    option_transmogrify<std::string>::register_from_python();

    to_python_converter<std::vector<std::string>, vector_transmogrify<std::string>>();
    vector_transmogrify<std::string>::register_from_python();

    to_python_converter<std::vector<double>, vector_transmogrify<double>>();
    vector_transmogrify<double>::register_from_python();

    to_python_converter<boost::optional<double>, option_transmogrify<double>>();
    option_transmogrify<double>::register_from_python();

    to_python_converter<NDSize, ndsize_transmogrify>();
    ndsize_transmogrify::register_from_python();
}
