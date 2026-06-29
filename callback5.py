use pyo3::prelude::*;
use pyo3::types::PyList;

/// This is the Rust implementation of the OptDispatchMP bottleneck.
/// It takes in raw data (e.g., lists of floats) and returns the processed data.
#[pyfunction]
fn rust_opt_dispatch_mp(py: Python, demands: Vec<f64>, capacities: Vec<f64>) -> PyResult<&PyList> {
    let mut optimized_dispatch = Vec::new();

    // The Bottleneck Logic: Rust will execute this loop exponentially faster than Python.
    for (i, &demand) in demands.iter().enumerate() {
        let capacity = capacities.get(i).unwrap_or(&0.0);
        
        // Example computation: heavy data massaging, filtering, or allocation logic
        let dispatch_value = if demand <= *capacity {
            demand
        } else {
            *capacity
        };
        
        optimized_dispatch.push(dispatch_value);
    }

    // Convert the Rust Vector back into a Python List so Pyomo can use it
    let py_list = PyList::new(py, &optimized_dispatch);
    Ok(py_list)
}

/// A Python module implemented in Rust. The name of this function must match
/// the `lib.name` setting in the `Cargo.toml`.
#[pymodule]
fn snl_progress_ext(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(rust_opt_dispatch_mp, m)?)?;
    Ok(())
}
