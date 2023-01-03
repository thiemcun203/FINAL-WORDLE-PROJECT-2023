import colorama
from colorama import Fore
colorama.init(autoreset=True)
import random
import matplotlib.pyplot as plt

def convert_ternary(feedback:list) -> int:
    """
    Parameters
    ----------
    feedback : list
        Contains 05 elements, which can be 0, 1, or 2, denoting a feedback pattern.
    -------
    Return 
    ------
    int
        Base 10 representation of pattern.
    """
    return sum([feedback[i]*3**(4-i) for i in range(5)])

def get_feedback(guess:str,answer:str) ->list:
    """
    Parameters
    ----------
    guess : str
        Five-letter guess.
    answer : str
        Five-letter correct answer.
    -------
    Return 
    ------
    feedback : list
        Contains 05 elements, which can be 0, 1, or 2, denoting a feedback pattern.
    """
    #convert string to list
    temp = list(answer)
    answer = temp
    temp = list(guess)
    guess = temp
    
    #initialize
    feedback = ['']*5
    #isolate correctly placed letters
    for i in range(5):
        if guess[i] == answer[i]:
            feedback[i] = 2
            answer[i] = ''
            guess[i] = ''
    
    #isolate wrongly placed letters
    for i in range(5):
        if guess[i] == '': continue
        elif guess[i] in answer:
            feedback[i] = 1
            answer[answer.index(guess[i])] = ''
            guess[i] = ''
        else:
            feedback[i] = 0
    return feedback

def reduce_list(guess:str,feedback:list,word_list:list) ->list:
    '''
    Parameters
    ----------
    guess: the word we guessed in this step
    feedback: the pattern given by game
    word_list: allowed list in the first step and the reduced list in the next steps
    ----------
    Return 
    ------
    the reduced word list which could be possible answers or allowed guesses in hardmode and possible answers in easymode
    
    '''
    return [word for word in word_list if get_feedback(guess,word)==feedback]


def generate_ternary(n:int) ->list:
    """
    Parameters
    ----------
    n: An integer, indicating length of number.
    
    ----------
    Return 
    ------
    res: List of all ternary numbers of length n.
    """
    res = list()
    s = [0] * n
    while True:
        temp = s[:]
        res.append(temp)
        i = n-1
        while i >= 0:
            if s[i] == 2:
                i -= 1
            else:
                break
        if i == -1:
            break
        else:
            temp = s[i]
            s[i] = temp + 1
            for j in range(i+1,n):
                s[j] = 0
    return res
def REDUCE_LIST(guess:list,real_feedback:list,still_valid_words:list,mode={0,1,2}):
    """
    Parameters
    ----------
    still_valid_words : list
        Contains words still possible as an answer.
    guess : str
        Five-letter guess.
    real_feedback : list
        Contains 05 elements, which can be 0, 1, or 2, denoting a feedback pattern.
    mode: set
        One of the seven filters: {0}, {1}, {2}, {0,1}, {0,2}, {1,2}, {0,1,2}

    Returns
    -------
    updated_allowed_words : list
        Updates allowed_words by retaining only words fitting the actual feedback.
    """
    n = 0
    accepted_feedback = real_feedback[:]
    
    #letter_feedback works like a mould, designated colors are retained, other positions can be changed arbitrary
    for i, letter_feedback in enumerate(real_feedback):
        if letter_feedback not in mode:
            n += 1
            accepted_feedback[i] = None
    
    accepted_feedbacks_enumerated = list()
    
    #generate_ternary(n) lists all combinations available to fill in the arbitrary positions
    for insertion in generate_ternary(n):
        temp = accepted_feedback[:]
        for i, letter_feedback in enumerate(temp):
            if letter_feedback == None:
                temp[i] = insertion.pop(0) #traverse left to right, popping a combination to fill in the mould
        accepted_feedbacks_enumerated.append(convert_ternary(temp))
    updated_allowed_words = list()
    for word in still_valid_words:
        feedback_enumerated = convert_ternary(get_feedback(guess,word))
        if feedback_enumerated in accepted_feedbacks_enumerated:
            updated_allowed_words.append(word)
    return updated_allowed_words

def check_win(feedback:list)->list:
    """
    Parameters
    ----------
    feedback : list
        Contains 05 elements, which can be 0, 1, or 2.
    ---------
    Return
    -------
    win : bool
        Becomes True when feedback is a list of 05 2's.
    """
    return feedback==[2]*5

def TestModel(solution_for_test,test_list:list,RANDOM=False) -> tuple:
    '''
    Parameter
    ----------
    solution: The function return the number of step to guess a specific answer \n
    test_list: The list of answers for testing
    RANDOM: False, answer is chosen randomly and True, answer is chosen sequentially from the test_list
    ----------
    Return: The bar chart with x(number of guesses needed) and y (number of plays having x guesses) \n
                  The tupple of winrate and average score'''
    import time
    t1=time.time()
    #Compute some vital factor: number of plays having x guesses, win rate, average score of 2,3k plays   
    xMax=20 # may be posituve infinity number
    yMax=0
    lst=[0]*xMax
    N=len(test_list)# list contains number of plays having x guesses
    for word in test_list:
        if not RANDOM:
            answer=word
        elif RANDOM:
            answer=random.choice(test_list)
        NumberOfGuessesNeeded=len(solution_for_test(answer))
        lst[NumberOfGuessesNeeded]=lst[NumberOfGuessesNeeded]+1
    winrate=sum(lst[1:7])/N*100
    average=sum([i*lst[i] for i in range(1,xMax)]) / N

    #VISUALIZATION
    for i in range(1,xMax):
        if lst[i] >=yMax: # because yMax always in (1,6)
            yMax=lst[i]
        if lst[i]==0 and i>6:
            xMax=i
            break
    yMax=(yMax//100+2)*100
    x=[str(i) for i in range(1,xMax)]
    y=[i for i in lst[1:xMax]]
    plt.ylim(0,yMax)
    plt.grid(axis='y',linestyle='--')
    plt.xlabel('Number of guesses needed')
    plt.ylabel('Number of plays having x guesses')
    plt.title('TEST PERFORMANCE')
    plt.bar(x,y, fc="#CCD6A6", ec="black")
    for i in range(len(x)):
        plt.text(i, y[i], y[i], ha="center", va="bottom")
    t2=time.time()
    time=t2-t1
    plt.text(xMax,yMax/2, f'Win Rate: {winrate:.3f}%\nAverage Score: {average:.3f}\nTime: {time:.3f}s', fontsize = 20,
		bbox = dict(facecolor = '#CCD6A6', alpha = 0.7))
    plt.show()
    return winrate,average

def print_guess_board(guess_board,feedback_board):
    print(' ___________')
    for i in range(6):
        print('|',end=' ')
        for j in range(5):
            if feedback_board[i][j] == 0:
                print(Fore.LIGHTBLACK_EX + guess_board[i][j], end=' ')
            elif feedback_board[i][j] == 1:
                print(Fore.LIGHTYELLOW_EX + guess_board[i][j], end=' ')
            elif feedback_board[i][j] == 2:
                print(Fore.GREEN + guess_board[i][j], end=' ')
            else:
                print(guess_board[i][j], end=' ')
        print('|')
    print('|___________|\n')

def reduce_allowed_words(allowed_words,guess,real_feedback):
    """
    

    Parameters
    ----------
    allowed_words : list
        Contains allowed guesses.
    guess : str
        Five-letter guess.
    real_feedback : list
        Contains 05 elements, which can be 0, 1, or 2, denoting a feedback pattern.

    Returns
    -------
    updated_allowed_words : list
        Updates allowed_words by retaining only words fitting the actual feedback.

    """
    real_feedback_enumerated = convert_ternary(real_feedback)
    updated_allowed_words = list()
    for word in allowed_words:
        feedback_enumerated = convert_ternary(get_feedback(guess,word))
        if feedback_enumerated == real_feedback_enumerated:
            updated_allowed_words.append(word)
    
    return updated_allowed_words
  


       


