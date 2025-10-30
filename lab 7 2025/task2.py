n = int(input()) # кол-во дней
prices = list(map(int, input().split())) # цены акций

# пока цена следующего дня больше, чем предыдущего, мы будем продавать
# складываем все монотонно увеличивающиеся сегменты на графике акций

profit = 0
for i in range(1, n):
    if prices[i - 1] < prices[i]:
        profit += prices[i] - prices[i - 1]

print(profit)