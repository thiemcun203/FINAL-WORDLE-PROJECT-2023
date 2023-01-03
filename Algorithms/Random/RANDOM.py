import sys
sys.path.append('Algorithms') #append parent folder, but small than main folder: FINAL WORDLE PROJECT
from Wordle import *
import os
allowed_guesses=os.path.abspath('Data/allowed_guesses.txt')

with open(allowed_guesses,'r') as file:
    allowed_guesses=[]
    for i in file:
        allowed_guesses.append(i[:5])
def solution_for_test(answer:str,word_list=allowed_guesses,mode={0,1,2}) -> list:
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
    while True:
        guess=random.choice(word_list)
        guesses_list.append(guess)
        feedback=get_feedback(guess,answer)
        if check_win(feedback):
            break
        word_list=REDUCE_LIST(guess,feedback,word_list,mode)
        
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
    
    while attempt_number <= 5:

        #print guess_board
        print('\n   WORDLE  ')
        print_guess_board(guess_board,feedback_board)
        print('Press "Enter" to WordleBot continue playing')
        input()

        print("Guess #" + str(attempt_number+1))
        
        print("There are",len(still_valid_words),"left in the guess space.")
        
        
        if len(still_valid_words) > 10:
            print("By picking randomly, these are some of the words in the guess space:")
            lst=[word for word in random.sample(still_valid_words,10)]
                
        else:
            print("These are the words left in the guess space:")
            lst=[word for word in still_valid_words]

        for word in lst:
            print(word)
        
        #display guess
        guess = lst[random.randint(0,len(lst)-1)]
        
        #update guess into guess_board
        guess_board.insert(attempt_number,list(guess))
        del guess_board[-1]

        #update feedback into feedback_board
        real_feedback = get_feedback(guess,answer)
        feedback_board.insert(attempt_number,real_feedback)
        del feedback_board[-1]
        
        if check_win(real_feedback) == True:
            break
        
        temp = REDUCE_LIST(guess,real_feedback,still_valid_words)
        still_valid_words = temp

        attempt_number += 1
        
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
    
    while attempt_number <= 5:

        #print guess_board
        print('\n   WORDLE  ')
        print_guess_board(guess_board,feedback_board)
        guess=input(f'Enter your {attempt_number+1}th guess\n(Enter "yes" if you need my support): ').lower()
        while guess not in still_valid_words :
            #support
            if guess =='yes':
                print("There are",len(still_valid_words),"left in the guess space.")
                
                if len(still_valid_words) > 10:
                    print("By picking randomly, these are some of the words in the guess space:")
                    lst=[word for word in random.sample(still_valid_words,10)]
                
                        
                else:
                    print("These are the words left in the guess space:")
                    lst=[word for word in still_valid_words]

                for word in lst:
                    print(word)
                        
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
        
        temp = REDUCE_LIST(guess,real_feedback,still_valid_words)
        still_valid_words = temp
        attempt_number += 1
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
    When you reach your answer or lose please enter something not 'yes' to end program
    '''
    still_valid_words = allowed_guesses
    guess_board = [["_"]*5 for i in range(6)]
    feedback_board = [[None]*5 for i in range(6)]
    attempt_number = 0
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

  
            temp = REDUCE_LIST(guess,real_feedback,still_valid_words)
            still_valid_words = temp
            mm=input('(Press "Enter" to continue or Enter "." to suggest):  ')

        #print suggestion    
        print('\n   WORDLE  ')
        print_guess_board(guess_board,feedback_board)
        print("There are",len(still_valid_words),"left in the guess space.")
        
        if len(still_valid_words) > 10:
            print("By picking randomly, these are some of the words in the guess space:")
            lst=[word for word in random.sample(still_valid_words,10)]
        else:
            print("These are the words left in the guess space:")
            lst=[word for word in still_valid_words]
        for word in lst:
            print(word)        
        
        sp=input('Enter "yes" if you need my support: ')
        
   
    


if __name__ == "__main__":
    
    # solution_for_test('happy')
    # solution_for_WordleBot()
    # solution_for_simulationgame()
    solution_for_realgame()
    
    # real_possible_answers=os.path.abspath('Data/real_possible_answers.txt')
    # with open(real_possible_answers,"r") as file:
    #     real_possible_answers=[]
    #     for i in file:
    #         real_possible_answers.append(i[:5])
    # TestModel(solution_for_test,real_possible_answers)

    
    
    
    
    



