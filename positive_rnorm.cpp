#include <Rcpp.h>
using namespace Rcpp;

// [[Rcpp::export]]
NumericVector positive_rnorm(int n, double mean, double sd) {
  // Specify out as a numeric vector of size n
  NumericVector out(n);
  
  // This loops over the elements of out
  for(int i = 0; i < n; i++) {
    // This loop keeps trying to generate a value
    do {
      // Call R's rnorm()
      out[i] = R::rnorm(mean,sd);
      // While the number is negative, keep trying
    } while(out[i]<0);
  }
  return out;
}

/*** R
  positive_rnorm(10, 2, 2)
*/
