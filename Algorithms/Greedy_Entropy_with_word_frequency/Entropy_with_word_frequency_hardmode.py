import sys
sys.path.append('Algorithms') #append parent folder, but small than main folder: FINAL WORDLE PROJECT
from Wordle import *
import os
import json
import numpy as np
from math import *

allowed_guesses=os.path.abspath('Data/allowed_guesses.txt')
with open(allowed_guesses,'r') as file:
    allowed_guesses=[]
    for i in file:
        allowed_guesses.append(i[:5])
freq_gg=os.path.abspath('Data/word_freq_ggdict.json')
with open(freq_gg) as file:
    word_freq_ggdict=json.load(file)
def sigmoid(x):
    return 1/(1+e**(-x))
CommonWord=3000
def get_freq(word_freq_ggdict:list,CommonWord=CommonWord,Width=10) -> dict:
    #make sorted word list by freq
    lst=list(word_freq_ggdict.items())
    lst.sort(key=lambda x: x[1])
    
    #add word into horizontal axis of sigmoid function
    N=len(word_freq_ggdict)
    metric = np.linspace(-Width*(N-CommonWord)/N,Width*CommonWord/N,N)
    priors=dict()
    for pair, unit in zip(lst,metric):
        priors[pair[0]]=sigmoid(unit)
    return priors
frequency=get_freq(word_freq_ggdict)
def entropy(guess:str, possible_answers:list):
    '''Function compute the entropy of each word which could be chosen in hard mode \n
    Return value of entropy(bits)'''
    Entropy=0
    pd_patterns = {} 
    total_freq=0
    # words_of_pattern={}
    for word in possible_answers:
        total_freq+=frequency[word]
    for word in possible_answers: 
        feedback = convert_ternary(get_feedback(guess,word))
        # words_of_pattern[feedback]=words_of_pattern.get(feedback,[])+[word]
        pd_patterns[feedback] = pd_patterns.get(feedback,0) +frequency[word]/total_freq
    for prob in pd_patterns.values():
        Entropy+=-prob*log2(prob)
    return Entropy
entropy('tares',allowed_guesses)

def entropy_dict(possible_answers):
    '''Function compute entropy of each word in list
    Return the rank of possible answer (result of entropy function) based value of entropy
    It may take less then 10 mins to compute for the first list - first guess'''
    ranker=[]
    for guess in possible_answers:
        ranker.append((guess,entropy(guess,possible_answers)))
    ranker.sort(key = lambda t: t[1], reverse = True)
    return ranker

firstguesses_freq=os.path.abspath('Data/firstguesses_freq.json')
def savefile():
    with open(firstguesses_freq,'w') as f:
        json.dump(entropy_dict(allowed_guesses),f)
#15m40.6s
def openfile():
    with open(firstguesses_freq,'r') as f:
        file=json.load(f)
    return file

fl=openfile()

def solution_for_test(answer:str,word_list=allowed_guesses) -> list:
    '''
    Parameters
    ----------
    answer: Five-letter actual answer.
    allowed_words: Contains ~13000 allowed guesses.
    mode: One of the seven filters: {0}, {1}, {2}, {0,1}, {0,2}, {1,2}, {0,1,2}
    --------
    Return
    -------
    tupple of guess_count and actual_guesses_list
    guesses_list: (list) list of guesses needed to reach the actual answer.
    '''
    guesses_list=[]
    word_list=allowed_guesses
    guess=fl[0][0]
    while True:
        guesses_list.append(guess)
        feedback=get_feedback(guess,answer)
        if check_win(feedback):
            break
        word_list=reduce_list(guess,feedback,word_list)
        guess=entropy_dict(word_list)[0][0]
    return guesses_list

def solution_for_WordleBot(allowed_guesses=allowed_guesses) ->list:
    '''
    This function will display the process of auto play of WordleBot
    
    ------
    Firstly, enter your answer to WordleBot try to guess
    Then press 'Enter' to look step by step
    '''
    answer = input('Enter a word for the WordleBot to guess: ').lower()
    while answer not in allowed_guesses:
        answer=input('Not a valid word - Please try again: ').lower()
    still_valid_words = allowed_guesses
    guess_board = [["_"]*5 for i in range(6)]
    feedback_board = [[None]*5 for i in range(6)]
    attempt_number = 0
    ranker=fl[:10]
    while attempt_number <= 5:

        #print guess_board
        print("\n Guess #" + str(attempt_number+1))
        print("There are",len(still_valid_words),"left in the guess space.")
        
        if len(still_valid_words) > 10:
            print("By picking first highest 10 words, these are some of the words in the guess space:")
            if attempt_number >0:
                ranker = entropy_dict(still_valid_words)[:10]
              
                        
        else:
            print("These are the words left in the guess space:")
            ranker=entropy_dict(still_valid_words)
            
        print(f'Word      Entropy')
        for pair in ranker:
            print(f'{pair[0]}     {pair[1]:.2f}')
        #display guess
        guess = ranker[0][0]
        
        #update guess into guess_board
        guess_board.insert(attempt_number,list(guess))
        del guess_board[-1]

        #update feedback into feedback_board
        real_feedback = get_feedback(guess,answer)
        feedback_board.insert(attempt_number,real_feedback)
        del feedback_board[-1]

        if check_win(real_feedback) == True:
            break
        
        
        temp=reduce_list(guess, real_feedback,still_valid_words)
        pactual= len(temp)/len(still_valid_words)
        actual_infor=-log2(pactual)
        still_valid_words=temp
        attempt_number += 1
        print('\n   WORDLE  ')
        print_guess_board(guess_board,feedback_board)
        print(f'Actual amount of information received (in bits): {actual_infor:.2f}')
        print(f'Remaining possibilities: {len(still_valid_words)}')
        input('Press "Enter" to WordleBot continue playing')

        
    print('\n   WORDLE  ')
    print_guess_board(guess_board,feedback_board)
    if check_win(real_feedback):
        print('Congratulation!!')
    else:
        print("Sorry, I'm trying to be better")
    
    
def solution_for_simulationgame() -> None:
    '''
    This function simulates the real game for user easly play and use our word suggestion functionality
    
    -------
    Player try to guess to reach answer like the real game by enter their guess as usual
    If they need suggested word: Enter "yes" then choose their own guess for the next step from list of suggested word
    '''
    real_possible_answers=os.path.abspath('Data/real_possible_answers.txt')
    with open(real_possible_answers,"r") as file:
        real_possible_answers=[]
        for i in file:
            real_possible_answers.append(i[:5])
    
    answer = random.choice(real_possible_answers)
    still_valid_words = allowed_guesses
    guess_board = [["_"]*5 for i in range(6)]
    feedback_board = [[None]*5 for i in range(6)]
    attempt_number = 0
    ranker=fl[:10]
    #print guess_board
    print('\n   WORDLE  ')
    print_guess_board(guess_board,feedback_board)
    
    while attempt_number <= 5:
        change=0
        guess=input(f'Enter your {attempt_number+1}th guess\n(Enter "yes" if you need my support): ').lower()
        while guess not in still_valid_words:
            #support
            if guess =='yes':
                change=1
                print("There are",len(still_valid_words),"left in the guess space.")
                
                if len(still_valid_words) > 10:
                    print("By picking first highest 10 words, these are some of the words in the guess space:")
                    if attempt_number >0:
                        ranker = entropy_dict(still_valid_words)[:10]
                
                else:
                    print("These are the words left in the guess space:")
                    ranker=entropy_dict(still_valid_words)
                
                print(f'Word      Entropy')
                for pair in ranker:
                    print(f'{pair[0]}     {pair[1]:.2f}')
                
                        
                #official guess input
                guess=input(f'Enter your {attempt_number+1}th guess: ').lower()
                
            else:
                guess=input('Not a valid word - Please try again: ').lower()
            
            
            
        #update guess into guess_board    
        guess_board.insert(attempt_number,list(guess))
        del guess_board[-1]
        
        #update feedback into feedback_board
        real_feedback = get_feedback(guess,answer)
        feedback_board.insert(attempt_number,real_feedback)
        del feedback_board[-1]
    
        if check_win(real_feedback) == True:
            break
        
        temp=reduce_list(guess, real_feedback,still_valid_words)
        pactual= len(temp)/len(still_valid_words)
        actual_infor=-log2(pactual)
        still_valid_words=temp
        attempt_number += 1
        print('\n   WORDLE  ')
        print_guess_board(guess_board,feedback_board)
        if change==1:
            print(f'Actual amount of information received (in bits): {actual_infor:.2f}')
            print(f'Remaining possibilities: {len(still_valid_words)}')
    
    print('\n   WORDLE  ')
    print_guess_board(guess_board,feedback_board)
    if check_win(real_feedback):
        print('Congratulation!!')
    else:
        print('Game over')
        
def solution_for_realgame()->None:
    '''
    This function help gamers have guess for the next step by enter your guesses and feedback
    
    ----------
    Enter "yes" if you need support
    
    ------
    When you choose press 'Enter' \n
    Then enter all guess you entered into real game and all corresponding feedback recieved from the real game
    Ex. guess: "tares" and feedback: "00210" (0: grey, 1: yellow, 2: green)
    ------
    When you choose enter '.' \n
    This function will return some suggested word for you to continue playing on real game
    
    -------
    If you still need suggested word for the next step then Enter '.'
    
    --------
    You dont need to retype all word typed before
    When you reach your answer or lose please enter something not 'yes' to end program
    '''
    still_valid_words = allowed_guesses
    guess_board = [["_"]*5 for i in range(6)]
    feedback_board = [[None]*5 for i in range(6)]
    attempt_number = 0
    ranker=fl[:10]
    sp=input('Enter "yes" if you need my support: ')
    
    # collect inputted then reduce guess space
    while sp=='yes':
        print('\n   WORDLE  ')
        print_guess_board(guess_board,feedback_board)
        print('Enter your guesses and feedback on real game')
        mm=input('(Press "Enter" to continue add more guesses or Enter "." to suggest):  ')
        while mm!=".":
            guess = input('guess: ').lower()
            while guess not in still_valid_words:
                guess=input('Not a valid word - Please try again: ').lower()
            feedback=input('Feedback: ')
            while len(feedback) !=5:
                feedback=input('Not a valid feedback - Please try again: ')

            #update guess into guess_board  
            guess_board.insert(attempt_number,list(guess))
            del guess_board[-1]
            
            #update feedback into feedback_board
            real_feedback = [int(i) for i in str(feedback)]
            feedback_board.insert(attempt_number,real_feedback)
            del feedback_board[-1]

  
            temp = reduce_list(guess,real_feedback,still_valid_words)
            still_valid_words = temp
            mm=input('(Press "Enter" to continue or Enter "." to suggest):  ')
            attempt_number+=1
        #print suggestion    
        print('\n   WORDLE  ')
        print_guess_board(guess_board,feedback_board)
        print("There are",len(still_valid_words),"left in the guess space.")
        if len(still_valid_words) > 10:
            print("By picking first highest 10 words, these are some of the words in the guess space:")
            if attempt_number >0:
                ranker = entropy_dict(still_valid_words)[:10]
        
        else:
            print("These are the words left in the guess space:")
            ranker=entropy_dict(still_valid_words)
        
        print(f'Word      Entropy')
        for pair in ranker:
            print(f'{pair[0]}     {pair[1]:.2f}')

        
        sp=input('Enter "yes" if you need my support: ')
        
   
    


if __name__ == "__main__":
    
    # print(solution_for_test('hence'))
    # solution_for_WordleBot()
    solution_for_simulationgame()
    # solution_for_realgame()
    
    # real_possible_answers=os.path.abspath('Data/real_possible_answers.txt')
    # with open(real_possible_answers,"r") as file:
    #     real_possible_answers=[]
    #     for i in file:
    #         real_possible_answers.append(i[:5])
    # TestModel(solution_for_test,real_possible_answers)

    
    
    
    
    



