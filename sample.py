def factorial(n):
	if n == 0:
		return 1

	return n * factorial(n-1)

def iterativeFactorial(n):
	result = 1
	for i in range(1,n+1):
		result = result * i

	return result



def main():
	print("The factorial of 5 is", factorial(5))
	print("The iterative factorial of 5 is", iterativeFactorial(5))

main()