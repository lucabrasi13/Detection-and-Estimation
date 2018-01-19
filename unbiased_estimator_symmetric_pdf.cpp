// C++ Program to test the symmetric pdf nature of an unbiased estimator for DC signal with noise
// Library used is it++

#include<iostream>
#include<itpp/itbase.h>
#include<itpp/signal/transforms.h> 
#include<itpp/stat/misc_stat.h>
#include<vector>

using namespace std;
using namespace itpp;

using std::cout;
using std::endl;

int writeITfile(vec a)
{
// Function to write it to a .it file to plot using Matlab or Octave for convenience	
	// Declare the IT file class
	it_file ff;
	// Open a new file
	ff.open("unbiased_symmetric_pdf_plot.it"); 
	// Add data to the file
	ff << Name("A_hat_iteration") <<a;
	// Force the file to be written into to the disk
	ff.flush();
	// Close the file
	ff.close();
	// Exit the program
	return 0;
}

int main()
{
// Define the signal
	// Define the DC component of the signal
	double A = 10;
	// Define the length of the signal
	int N = 10;
	// Define and intialize the signal vector
	vec x(N);
	x = zeros(N);

// Define a few parameters for the simulation
	// Define the number of iterations
	int numIteration = 1000;
	// Define the mean and variance of Noise
	double mu = 0, sigma = 1;
	// Define the Estimator vector used in the simulation
	vec A_hat_iteration = zeros(numIteration);
	// Define the Estimator vector
	double A_hat;

// Start the simulation
	// Define a few parameters
	int i;
	for(i=1;i<numIteration;i++)
	{
	// Add noise to the signal
		x = A + Normal_RNG(mu,sigma)(N);
	// Estimate the DC Value
		A_hat_iteration[i] = mean(x);
	}
// Write the data from A_hat_iteration to a .it file to plot the histogram
	writeITfile(A_hat_iteration);

// Find the Expected value of the estimator
	A_hat = mean(A_hat_iteration);

// Print the Estimated value
	cout << "The Estimated DC value is " << double(A_hat) << endl; 			
	return 0;
} 
