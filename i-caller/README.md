# Graph-Based in Spam Call Detection

## Dataset

| Name            | IsMember          | Type    |
| --------------- | ----------------- | ------- |
| str             | bool              | int     |
| '+841234567890' | True/False or 0/1 | Table 1 |

**Type:**

| Type | Description | Type | Description |
| ---- | ----------- | ---- | ----------- |
| 0    | Trusted     | 4    | Cheat       |
| 1    | Advertising | 5    | Estate      |
| 2    | Loan        | 6    | Others      |
| 4    | Debt        | -1   | Undefined   |

## Summary

### Graph Statistics

| Attributes | Value   |
| ---------- | ------- |
| Nodes      | 288,972 |
| Node Types | 6       |
| Edges      | 461,790 |
| Edge Types | 1       |

#### Degree Distribution

<img src="Graph-Based in Spam Call Detection.assets/Degree Distribution-1618043346764.png" alt="Degree Distribution" style="zoom: 2%;" />

Degree Distribution: Exponential Distribution $\Rightarrow$ `Scale-free Model`

### Types Summary

#### CallRank value

##### CallRank Distribution each Type

<img src="Graph-Based in Spam Call Detection.assets/CallRank Distribution-1618043938995.png" alt="CallRank Distribution" style="zoom:6%;" />

Only Spammers

<img src="Graph-Based in Spam Call Detection.assets/CallRank Distribution (only Spammers).png" alt="CallRank Distribution (only Spammers)" style="zoom:6%;" />

#### Confidence Interval

> Suppose CallRank of each type is following Poisson Distribution

| Type           | CI                |
| -------------- | ----------------- |
| TrustedUser    | 13.5124 - 16.5124 |
| EstateSpammers | 0.1318 - 2.1318   |
| DebtSpammers   | 0.6488 - 2.6488   |
| LoanSpammers   | 0.1554 - 2.1554   |
| CheatSpammers  | 0.1318 - 2.1318   |
| AdvertSpammers | 1.6086 - 3.6086   |
| OthersSpammers | 3.5711 - 5.5711   |

