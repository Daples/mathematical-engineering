def sol(n,a,b,c):
	if n==0 or (n<a and n<b and n<c):
		return 0
	res = sol(n-a,a,b,c)+1
	res = max(res, sol(n-b,a,b,c)+1)
	res = max(res, sol(n-c,a,b,c)+1)
	return res

print(str(sol(14,7,3,2)))
