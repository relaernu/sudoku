class sudoku:
    def __init__(self, list1 = []):
        if len(list1) !=0 and len(list1) != 81:
            raise ValueError("List length must be 0 or 81")
        self.Values = []
        if len(list1) == 0:
            for i in range(0,81):
                self.Values.append(0)
        else:
            for i in range(0,81):
                self.Values.append(list1[i])

    def Show(self):
        for i in range(0,9):
            print(self.GetRow(i))

    def FillWithList(self, list1):
        if len(list1) != 81:
            raise ValueError("List length must be 81") 
        for i in range(0,81):
            self.Values.append(list1[i])

    def GetRow(self, rownum):
        return self.Values[rownum*9: rownum*9+9]

    def GetCol(self, colnum):
        col = []
        for i in range(0,9):
            col.append(self.Values[i*9+colnum])
        return col

    def GetCell(self, rownum, colnum):
        row = self.GetRow(rownum)
        return row[colnum]

    def SetRow(self, rownum, values):
        if len(values) != 9:
            raise ValueError("Values must be 9 elements.")
        else:
            rowstart = rownum*9
            for i in range(rowstart, rowstart+9):
                self.Values[i] = values[i-rowstart]

    def SetCol(self, colnum, values):
        if len(values) != 9:
            raise ValueError("Values must be 9 elements.")
        else:
            for i in range(0,9):
                self.Values[i*9+colnum] = values[i]        

    def SetCell(self, rownum, colnum, value):
        self.Values[rownum*9 + colnum] = value


    def GetSquare(self, sqrnum):
        sqr = []
        for i in range(0,3):
            row = int(sqrnum/3) * 3 + i
            for j in range(0,3):
                col = sqrnum%3 * 3 + j
                sqr.append(self.GetCell(row, col))
        return sqr

    def GetSqrNum(self, rownum, colnum):
        return int(rownum/3)*3 + int(colnum/3)

    def ShiftLeft(self, vlist):
        vfirst = vlist.pop(0)
        vlist.append(vfirst)

    def LogicAnd(self, list1, list2):
        list1.sort()
        list2.sort()
        andset = []
        for l1 in list1:
            if l1 != 0:
                for l2 in list2:
                    if l2 != 0:
                        if l2 == l1:
                            andset.append(l2)
                            break
        return andset

    def LogicOr(self, list1, list2):
        list1.sort()
        list2.sort()
        orset = []
        for l1 in list1:
            if l1 != 0:
                if not l1 in orset:
                    orset.append(l1)
        for l2 in list2:
            if l2 != 0:
                if not l2 in orset:
                    orset.append(l2)
        orset.sort()
        return orset

    def LogicXor(self, list1, list2):
        andset = self.LogicAnd(list1, list2)
        xorset = []
        for l1 in list1:
            if l1 != 0:
                if not l1 in andset:
                    xorset.append(l1)
        for l2 in list2:
            if l2 != 0:
                if not l2 in andset:
                    xorset.append(l2)
        xorset.sort()
        return xorset

    def GetCellAvail(self, rownum, colnum):
        numbers = [1,2,3,4,5,6,7,8,9]
        avail = []
        cell = self.GetCell(rownum, colnum)
        if  cell != 0:
            avail.append(cell)
        else:
            sqrnum = self.GetSqrNum(rownum, colnum)
            avail = self.LogicXor(self.GetRow(rownum), numbers)
            avail = self.LogicAnd(self.LogicXor(self.GetCol(colnum), numbers), avail)
            avail = self.LogicAnd(self.LogicXor(self.GetSquare(sqrnum),numbers), avail)
        return avail

    def RemoveEmpty(self, list1):
        return [x for x in list1 if x != 0]

    def RowScan(self, rownum):
        dedicate = []
        row = self.GetRow(rownum)
        current_col = 0
        for i in range(0,9):
            if len(row[i]) != 1:
                current_col = i
                for n in row[i]:
                    duplicate = False
                    for k in range(0, 9):
                        if k != i:
                            if n in row[k]:
                                duplicate = True
                                break
                    if not duplicate:
                        dedicate.append((rownum, current_col, n))
        return dedicate
    
    def ColScan(self, colnum):
        dedicate = []
        col = self.GetCol(colnum)
        current_row = 0
        for i in range(0,9):
            if len(col[i]) != 1:
                current_row = i
                for n in col[i]:
                    duplicate = False
                    for k in range(0,9):
                        if k != i:
                            if n in col[k]:
                                duplicate = True
                                break
                    if not duplicate:
                        dedicate.append((current_row, colnum, n))
        return dedicate

    def SqrScan(self, sqrnum):
        dedicate = []
        sqr = self.GetSquare(sqrnum)
        for r in range(0,3):
            for c in range(0,3):
                row = int(sqrnum/3)*3 + r
                col = (sqrnum%3)*3 + c
                i = r * 3  + c
                if len(sqr[i]) != 1:
                    for n in sqr[i]:
                        duplicate = False
                        for k in range(0,9):
                            if k != i:
                                if n in sqr[k]:
                                    duplicate = True
                                    break
                        if not duplicate:
                            dedicate.append((row, col, n))
        return dedicate
                
    def ConvertList(self):
        self.Values = [x[0] if len(x) == 1 else 0 for x in self.Values]

    def GetDedicates(self):
        dedicates = []
        for i in range(0,9):
            dedicates.extend(self.RowScan(i))
            dedicates.extend(self.ColScan(i))
            dedicates.extend(self.SqrScan(i))
        return dedicates

    def GetFitLists(self):
        fitlist = []
        for r in range(0,9):    
            for c in range(0,9):
                fitlist.append(self.GetCellAvail(r,c))
        return fitlist
    
    def CountZero(self):
        return self.Values.count(0)

    def Solve(self):
        last_zero = self.Values.count(0)
        print(f"Initial: {last_zero}")
        cycle = 1
        while last_zero != 0:
            self.Values = self.GetFitLists()
            dedicates = self.GetDedicates()
            self.ConvertList()
            for l in dedicates:
                self.SetCell(l[0],l[1],l[2])
            print(f"Cycle: {cycle}, Zero Count: {self.Values.count(0)}")
            if last_zero == self.Values.count(0):
                print("Error: No solution or more than 1 solution.")
                break
            last_zero = self.Values.count(0)
            cycle = cycle + 1
        self.Show()
        
