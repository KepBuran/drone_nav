import numpy as np

class HungarianAlgorithm:
    def __init__(self, mat):
        self.mat = mat

    def min_zero_row(self, zero_mat, mark_zero):
        min_row = [99999, -1]
        for row_num in range(zero_mat.shape[0]): 
            if np.sum(zero_mat[row_num] == True) > 0 and min_row[0] > np.sum(zero_mat[row_num] == True):
                min_row = [np.sum(zero_mat[row_num] == True), row_num]
        zero_index = np.where(zero_mat[min_row[1]] == True)[0][0]
        mark_zero.append((min_row[1], zero_index))
        zero_mat[min_row[1], :] = False
        zero_mat[:, zero_index] = False

    def mark_matrix(self):
        cur_mat = self.mat
        zero_bool_mat = (cur_mat == 0)
        zero_bool_mat_copy = zero_bool_mat.copy()
        marked_zero = []
        while (True in zero_bool_mat_copy):
            self.min_zero_row(zero_bool_mat_copy, marked_zero)
        marked_zero_row = []
        marked_zero_col = []
        for i in range(len(marked_zero)):
            marked_zero_row.append(marked_zero[i][0])
            marked_zero_col.append(marked_zero[i][1])
        non_marked_row = list(set(range(cur_mat.shape[0])) - set(marked_zero_row))
        marked_cols = []
        check_switch = True
        while check_switch:
            check_switch = False
            for i in range(len(non_marked_row)):
                row_array = zero_bool_mat[non_marked_row[i], :]
                for j in range(row_array.shape[0]):
                    if row_array[j] == True and j not in marked_cols:
                        marked_cols.append(j)
                        check_switch = True
            for row_num, col_num in marked_zero:
                if row_num not in non_marked_row and col_num in marked_cols:
                    non_marked_row.append(row_num)
                    check_switch = True
        marked_rows = list(set(range(self.mat.shape[0])) - set(non_marked_row))
        return marked_zero, marked_rows, marked_cols

    def adjust_matrix(self, cover_rows, cover_cols):
        cur_mat = self.mat
        non_zero_element = []
        for row in range(len(cur_mat)):
            if row not in cover_rows:
                for i in range(len(cur_mat[row])):
                    if i not in cover_cols:
                        non_zero_element.append(cur_mat[row][i])
        min_num = min(non_zero_element)
        for row in range(len(cur_mat)):
            if row not in cover_rows:
                for i in range(len(cur_mat[row])):
                    if i not in cover_cols:
                        cur_mat[row, i] = cur_mat[row, i] - min_num
        for row in range(len(cover_rows)):  
            for col in range(len(cover_cols)):
                cur_mat[cover_rows[row], cover_cols[col]] = cur_mat[cover_rows[row], cover_cols[col]] + min_num
        return cur_mat

    def solve(self): 
        dim = self.mat.shape[0]
        cur_mat = self.mat
        for row_num in range(self.mat.shape[0]): 
            cur_mat[row_num] = cur_mat[row_num] - np.min(cur_mat[row_num])
        for col_num in range(self.mat.shape[1]): 
            cur_mat[:,col_num] = cur_mat[:,col_num] - np.min(cur_mat[:,col_num])
        zero_count = 0
        while zero_count < dim:
            ans_pos, marked_rows, marked_cols = self.mark_matrix()
            zero_count = len(marked_rows) + len(marked_cols)
            if zero_count < dim:
                cur_mat = self.adjust_matrix(marked_rows, marked_cols)
        return ans_pos

    def ans_calculation(self, pos):
        total = 0
        ans_mat = np.zeros((self.mat.shape[0], self.mat.shape[1]))
        for i in range(len(pos)):
            total += self.mat[pos[i][0], pos[i][1]]
            ans_mat[pos[i][0], pos[i][1]] = self.mat[pos[i][0], pos[i][1]]
        return total, ans_mat