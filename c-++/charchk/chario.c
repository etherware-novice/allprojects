#include <stdio.h>

main()
{
	int c;

	while ((c = getchar()) != EOF)
		putchar(c);
	/* putchar(c); */
	printf("%d\n", c); 
}
