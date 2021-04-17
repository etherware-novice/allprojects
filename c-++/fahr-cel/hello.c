#include <stdio.h>

main()
{
	float fahr, celcius;
	int lower, upper, step;

	lower = 0; /* lower limit of temperature table */
	upper = 300; /* upper limit */
	step = 20; /* step size */

	fahr = lower;

	printf("F \t C\n");
	while ( fahr <= upper) {
		celcius = (5.0 / 9.0) * (fahr - 32.0);
		printf("%3.0f %6.1f\n", fahr, celcius);
		fahr = fahr + step;
	}	
}
