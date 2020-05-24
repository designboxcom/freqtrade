# Performance notes

## May 2020

3 strategies:
* bbl3h2rsistd.py
* bbl3h3rsisharpe.py
* bbrsi.py

### Context

During the COVID-19 crisis, BTC value decreased a lot, so the performance of
all the strategies was bad (between -2% and about 0%, equiv. to -150e to -16e).

#### bbl3h2rsistd

Buy at BB lower band 3 std deviation and sell at BB high band 2 std dev,
optimized with the default loss function. Also both RSI and MFI are required
at certain levels, for both buying and selling.

This performed the best, after 3 weeks the loss is about 0, when it went to
down to -2% (maybe more) at some point.

#### bbl3h3rsisharpe

Buy at BB lower band 3 std deviation and sell at BB high band 3 std dev,
optimized with the Sharpe ratio. Also both RSI and MFI are required
at certain levels, for both buying and selling.

This performed the worst, I guess the selling signal at high band 3 is too
stringent.

#### bbrsi

Basic BB lower band 3 and sell at BB middleband (example from Udemy course).
Only RSI is required, for both buying and selling.

It performed better than bbl3h3rsisharpe, most certainly thanks to the easier
selling signal.

### statistics

#### bbl3h2rsistd

ROI: Close trades
∙ 0.00090434 BTC (0.16%)
∙ 7.696 EUR
ROI: All trades
∙ -0.00192818 BTC (-0.33%)
∙ -16.410 EUR
Total Trade Count: 58
First Trade opened: 3 weeks ago
Latest Trade opened: 2 days ago
Avg. Duration: 3 days, 22:24:17
Best Performing: HIVE/BTC: 15.81%

#### bbl3h3rsisharpe

ROI: Close trades
∙ -0.01692793 BTC (-2.68%)
∙ -144.143 EUR
ROI: All trades
∙ -0.01692793 BTC (-2.68%)
∙ -144.143 EUR
Total Trade Count: 63
First Trade opened: 3 weeks ago
Latest Trade opened: 2 days ago
Avg. Duration: 2 days, 12:54:09
Best Performing: ERD/BTC: 11.02%

#### bbrsi

ROI: Close trades
∙ -0.01587037 BTC (-1.89%)
∙ -135.138 EUR
ROI: All trades
∙ -0.01587037 BTC (-1.89%)
∙ -135.138 EUR
Total Trade Count: 84
First Trade opened: 3 weeks ago
Latest Trade opened: 2 days ago
Avg. Duration: 1 day, 20:37:31
Best Performing: ERD/BTC: 11.02%

#### Performance comparison

bbl3h2rsistd              bbl3h3rsisharpe          bbrsi

1. HIVE/BTC 15.81% (2)    1. ERD/BTC 11.02% (2)    1. ERD/BTC 11.02% (2)
2. SC/BTC 14.06% (1)      2. SC/BTC 9.30% (1)      2. XZC/BTC 10.36% (1)
3. ERD/BTC 10.89% (1)     3. XZC/BTC 7.94% (1)     3. SC/BTC 9.30% (1)
4. STX/BTC 10.82% (1)     4. MANA/BTC 4.96% (2)    4. ATOM/BTC 5.06% (3)
5. FTM/BTC 10.65% (1)     5. HIVE/BTC 4.51% (2)    5. MANA/BTC 4.96% (2)
6. XZC/BTC 10.62% (1)     6. FET/BTC 4.25% (1)     6. IOTA/BTC 4.89% (2)
7. POWR/BTC 10.58% (1)    7. FTM/BTC 4.14% (1)     7. FET/BTC 4.25% (1)
8. MANA/BTC 8.17% (2)     8. MATIC/BTC 4.02% (1)   8. FTM/BTC 4.14% (1)
9. ONE/BTC 7.48% (1)      9. ONE/BTC 3.64% (1)     9. MATIC/BTC 4.02% (1)
10. ETC/BTC 6.13% (2)     10. ETH/BTC 3.17% (2)    10. ETH/BTC 3.20% (2)
11. AION/BTC 5.65% (1)    11. IOTX/BTC 3.02% (1)   11. IOTX/BTC 3.02% (1)
12. COS/BTC 5.15% (1)     12. SNT/BTC 2.98% (2)    12. SNT/BTC 2.98% (2)
13. ICX/BTC 5.01% (1)     13. BEAM/BTC 2.85% (1)   13. HIVE/BTC 2.72% (2)
14. SNT/BTC 4.98% (1)     14. POWR/BTC 2.56% (1)   14. POWR/BTC 2.56% (1)
15. MATIC/BTC 4.95% (1)   15. AION/BTC 2.55% (1)   15. XLM/BTC 2.54% (1)
16. SOL/BTC 4.82% (1)     16. XLM/BTC 2.54% (1)    16. DATA/BTC 2.44% (1)
17. IOTA/BTC 4.77% (1)    17. IOTA/BTC 2.48% (1)   17. ZRX/BTC 2.43% (1)
18. FET/BTC 4.74% (1)     18. ZRX/BTC 2.46% (1)    18. ETC/BTC 1.13% (3)
19. STEEM/BTC 2.60% (1)   19. ETC/BTC 1.10% (2)    19. OST/BTC 1.05% (1)
20. WTC/BTC 1.94% (1)     20. OST/BTC 1.05% (1)    20. BAT/BTC 0.74% (1)
21. WAVES/BTC 1.67% (1)   21. KMD/BTC 0.94% (1)    21. ONT/BTC 0.73% (1)
22. OST/BTC 1.05% (1)     22. GXS/BTC 0.29% (1)    22. LTO/BTC 0.56% (1)
23. KMD/BTC 0.94% (1)     23. ICX/BTC 0.14% (1)    23. KAVA/BTC 0.34% (1)
24. QTUM/BTC 0.93% (1)    24. QTUM/BTC 0.11% (1)   24. ICX/BTC 0.11% (1)
25. ETH/BTC 0.85% (1)     25. SOL/BTC 0.03% (1)    25. MTL/BTC 0.08% (1)
26. XRP/BTC 0.74% (3)     26. STEEM/BTC 0.02% (1)  26. QTUM/BTC 0.05% (1)
27. GXS/BTC 0.69% (1)     27. VIB/BTC -0.84% (1)   27. SOL/BTC 0.04% (1)
28. RVN/BTC 0.27% (1)     28. XRP/BTC -0.90% (2)   28. DASH/BTC 0.03% (1)
29. ALGO/BTC 0.11% (1)    29. XTZ/BTC -2.11% (2)   29. STEEM/BTC 0.02% (1)
30. BEAM/BTC 0.11% (1)    30. BCH/BTC -2.22% (2)   30. WRX/BTC 0.02% (1)
31. ZRX/BTC 0.11% (1)     31. ALGO/BTC -2.59% (2)  31. AION/BTC -1.56% (2)
32. BCH/BTC 0.09% (2)     32. RVN/BTC -3.51% (1)   32. BCH/BTC -1.96% (2)
33. NAS/BTC 0.08% (1)     33. NANO/BTC -5.22% (1)  33. BEAM/BTC -1.97% (2)
34. XMR/BTC 0.06% (1)     34. STRAT/BTC -9.36% (3) 34. XTZ/BTC -2.12% (1)
35. ARN/BTC 0.03% (1)     35. LINK/BTC -11.91% (1) 35. ALGO/BTC -2.42% (2)
36. XTZ/BTC 0.02% (1)     36. COTI/BTC -15.88% (1) 36. LEND/BTC -2.58% (1)
37. BTG/BTC 0.01% (1)     37. XMR/BTC -15.96% (1)  37. RVN/BTC -3.51% (1)
38. NANO/BTC -0.73% (1)   38. INS/BTC -16.95% (2)  38. NANO/BTC -3.63% (1)
39. VIB/BTC -0.84% (1)    39. NAS/BTC -17.48% (1)  39. MCO/BTC -3.83% (2)
40. REN/BTC -2.14% (1)    40. WRX/BTC -18.56% (2)  40. ARN/BTC -4.13% (1)
41. IOTX/BTC -3.42% (1)   41. ARN/BTC -19.15% (1)  41. NAS/BTC -4.51% (2)
42. LINK/BTC -8.13% (1)   42. DASH/BTC -19.26% (1) 42. XRP/BTC -4.98% (4)
43. INS/BTC -26.55% (1)   43. TNT/BTC -21.89% (4)  43. XMR/BTC -5.70% (2)
44. OGN/BTC -26.57% (2)   44. GRS/BTC -29.54% (1)  44. GXS/BTC -6.85% (2)
45. COTI/BTC -26.58% (1)  45. OGN/BTC -37.83% (2)  45. WTC/BTC -6.99% (2)
46. TNT/BTC -26.77% (3)                            46. WABI/BTC -7.22% (1)
47. GRS/BTC -26.78% (1)                            47. BTG/BTC -8.11% (2)
                                                   48. STRAT/BTC -9.39% (3)
                                                   49. ONE/BTC -9.86% (1)
                                                   50. INS/BTC -13.64% (3)
                                                   51. KMD/BTC -13.99% (1)
                                                   52. COTI/BTC -15.88% (1)
                                                   53. OGN/BTC -24.07% (2)
                                                   54. GRS/BTC -30.43% (1)
                                                   55. TNT/BTC -54.01% (2)

### Conclusions

Over 3 weeks in a particularly difficult context, the bbl3h2 was robust. It
is strange that bbrsi performed so badly compared to the bbl3h2, maybe
because the sell signal is too early?

Things to consider:
* It seems that the stop loss is not active, to check
* Not sure if both MFI and RSI are useful together
* Selling at h3 seems too late
