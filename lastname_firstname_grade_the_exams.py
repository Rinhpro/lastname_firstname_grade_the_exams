import pandas as pd
import numpy as np
import re
def analyst(f):
    count_row = 0
    error1_row = []
    error2_row = []
    valid_row = []
    for line in f:
        line = line.rstrip()
        count_row += 1
        #Kiểm tra các dòng dữ liệu thuộc lỗi 1/2/đúng->add vào list tương ứng
        if len(re.findall(',', line))!= 25:
            error1_row.append(line)
        elif not re.search('^N[0-9]{8,8}', line):
            error2_row.append(line)
        else: 
            valid_row.append(line)
    print('**** ANALYZING ****')
    if len(error1_row) + len(error2_row) == 0: 
        print('No errors found!')
    else:
        for row in error1_row: 
            print('Invalid line of data: does not contain exactly 26 values:\n', row)
        for row in error2_row: 
            print('Invalid line of data: N# is invalid:\n', row)
    print('**** REPORT ****')
    print('Total lines of data:', count_row)
    print('Total valid lines of data: {}'.format(len(valid_row)))
    print('Total invalid lines of data: {}'.format(len(error1_row) + len(error2_row)))
    f.close()
    #Trả về các list cần thiết để chạy hàm report
    return count_row, error1_row, error2_row, valid_row
def report(count_row, error1_row, error2_row, valid_row):
    answer_key = "B,A,D,D,C,B,D,A,C,C,D,B,A,B,A,C,B,D,A,C,A,A,B,D,D"
    list_key = answer_key.split(',')
    d1 = dict()
    skip = []
    wrong = []
    #So sánh từ phần tử của list answers với list_key rồi gán giá trị cho các phần tử đúng/sai/trống
    for i in valid_row:
        elements = i.split(',')
        Ma_sv = elements[0]
        answers = elements[1:]
        for i in range(len(answers)):
            if answers[i] == list_key[i]: answers[i] = 4
            elif answers[i] == '':
                answers[i] = 0
                skip.append(i+1)
            elif answers[i] != list_key[i]: 
                answers[i] = -1
                wrong.append(i+1)
        #Tạo 1 dict với key = mã SV, value = điểm số (tổng của list answers khi mà các phần tử đã được thay bằng điểm)
        d1[Ma_sv] = sum(answers)
    #Lấy ra list điểm sv để tính toán, in ra các yêu cầu
    list_score = [v for k,v in d1.items()]
    hs_gioi = [i>80 for i in list_score]
    print(f'Total student of high scores: {sum(hs_gioi)}')
    print(f'Mean (average) score: {sum(list_score)/len(list_score)}')
    print(f'Highest score: {max(list_score)}')
    print(f'Lowest score: {min(list_score)}')
    print(f'Range of scores: {max(list_score) - min(list_score)}')
    #tim median
    list_score.sort()
    if len(list_score)%2 != 0:
        i = len(list_score)//2
        median = list_score[i]
    else:
        i = len(list_score)//2
        median = (list_score[i] + list_score[i-1])/2
    print(f'Median score: {median}')
    #most skip answer
    #Ý tưởng: tạo 1 dict key = mã câu hỏi, value = tần suất bị skip
    skip.sort()
    d_skip = dict()
    most_skip = []
    for i in skip:
        d_skip[i] = d_skip.get(i, 0) + 1
    #Nếu mã câu hỏi có tần số = tần số lớn nhất-> add câu đó vào list most_skip
    for k,v in d_skip.items():
        if v == max(d_skip.values()):
            most_skip.append((f'{k}-{v}-{round(v/len(valid_row),2)}'))
    print('Question that most people skip:', ', '.join(most_skip))
    #most wrong answer
    wrong.sort()
    d_wrong = dict()
    most_wrong = []
    for i in wrong:
        d_wrong[i] = d_wrong.get(i, 0) + 1
    for k,v in d_wrong.items():
        if v == max(d_wrong.values()):
            most_wrong.append((f'{k}-{v}-{round(v/len(valid_row),2)}'))
    print('Question that most people answer incorrectly', ', '.join(most_wrong))
    return d1
def write(path, d1):
    with open(path+'_grades.txt','w') as f1:
        for k,v in d1.items():
            f1.write(k + ',' + str(v) + '\n')
    print('File had been written')
    f1.close()
    f1 = open(path+'_grades.txt','r')
    print(f1.read())
    f1.close()

def main():
    file_name = input('Enter file name: ')
    try: 
        f = open(file_name+'.txt', 'r')
        print('Successfully opened', file_name)
    except:
        print('File cannot be found.')
        return
    count_row, error1_row, error2_row, valid_row = analyst(f)
    d1 = report(count_row, error1_row, error2_row, valid_row)
    write(file_name, d1)
if __name__ == "__main__":
    main()