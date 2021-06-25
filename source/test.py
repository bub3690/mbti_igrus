# list 종류 E_I,S_N,T_F,J_P  각 리스트의 값이 0이면 앞, 1이면 뒤와 대응
# ex)E_I=[1,0]면 1->I, 0->E에 대응
E_I = [0,0,0,0,0,0,0,0,0,0]
S_N = [0,0,0,0,0,0,0,0,0,0]
T_F = [0,0,0,0,0,0,0,0,0,0]
J_P = [0,0,0,0,0,0,0,0,0,0]

# 각 선택지의 개수
E = 0
I = 0
S = 0
N = 0
T = 0
F = 0
J = 0
P = 0
mbti = 0

for j in E_I:
    if j == 0:
        E += 1
    elif j == 1:
        I += 1

for j in S_N:
    if j == 0:
        S += 1
    elif j == 1:
        N += 1

for j in T_F:
    if j == 0:
        T += 1
    elif j == 1:
        F += 1

for j in J_P:
    if j == 0:
        J += 1
    elif j == 1:
        P += 1

if E >= I and S > N and T > F and J <= P:
    mbti = 'ESTP'
elif E >= I and S > N and T <= F and J <= P:
    mbti = 'ESFP'
elif E >= I and S <= N and T <= F and J <= P:
    MBTI = 'ENFP'
elif E >= I and S <= N and T > F and J <= P:
    mbti = 'ENTP'
elif E >= I and S > N and T > F and J > P:
    mbti = 'ESTJ'
elif E >= I and S > N and T <= F and J > P:
    mbti = 'ESFJ'
elif E >= I and S <= N and T <= F and J > P:
    mbti = 'ENFJ'
elif E >= I and S <= N and T > F and J > P:
    mbti = 'ENTJ'
elif E < I and S > N and T > F and J > P:
    mbti = 'ISTJ'
elif E < I and S > N and T <= F and J > P:
    mbti = 'ISFJ'
elif E < I and S <= N and T <= F and J > P:
    mbti = 'INFJ'
elif E < I and S <= N and T > F and J > P:
    mbti = 'INTJ'
elif E < I and S > N and T > F and J <= P:
    mbti = 'ISTP'
elif E < I and S > N and T <= F and J <= P:
    mbti = 'ISFP'
elif E < I and S <= N and T <= F and J <= P:
    mbti = 'INFP'
elif E < I and S <= N and T > F and J <= P:
    mbti = 'INTP'

print(mbti)