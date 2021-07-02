#include <stdio.h>
#include <string.h>

int main() {
	char *p, str[] = "hello world!";
	int i;
	p = &str[0];

	for(i = 0; i < strlen(str); i++){
		printf("%c", *p++);
	}
}
