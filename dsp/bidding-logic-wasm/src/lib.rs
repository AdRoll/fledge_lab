use wasm_bindgen::prelude::*;

// return type must be f64 otherwise the function does not even get
// recognized when being called from the browser, this corresponds to
// JS's definition of the number type:
// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#number_type
#[wasm_bindgen]
pub fn bid(bid: i32) -> f64 {
    bid.into()
}

#[wasm_bindgen]
pub fn do_nothing() {

}
