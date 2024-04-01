import numpy_financial as npf
import numpy as np

Rate = 0.07
Nper = 5
Loan_Amount = 650000.00
bbalance = Loan_Amount

Total_PMT = -npf.pmt(Rate/12, Nper*12, Loan_Amount, 0)
Cum_Interest = np.cumsum([npf.ipmt(Rate/12, i, Nper*12, Loan_Amount) for i in range(1, Nper*12 + 1)])

count = 1
while bbalance > 0:
    ppmt = -npf.ppmt(Rate/12, count, Nper*12, Loan_Amount)
    ipmt = -npf.ipmt(Rate/12, count, Nper*12, Loan_Amount)
    ebalance = bbalance - ppmt
    print("Period:", count)
    print("Principal Payment:", ppmt)
    print("Cumulative Interest:", Cum_Interest[count - 1])
    print("Remaining Balance:", ebalance)
    print("-------------------")
    bbalance = ebalance
    count += 1


    