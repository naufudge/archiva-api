from bs4 import BeautifulSoup
import httpx

def get_exchange_rates():
    mma_crossrates, mma_exchange_rates = "http://www.mma.gov.mv/crossrates.php", "http://www.mma.gov.mv/#/statistics/exchangerates"

    timeout = httpx.Timeout(5, read_timeout=None, connect_timeout=None)
    client = httpx.Client(http2=True, timeout=timeout)
    page_crossrates = client.get(mma_crossrates)

    soup = BeautifulSoup(page_crossrates.content, 'html.parser')
    crossrates_rows = soup.find_all('tr')


    mvr_to_dollar = 15.42 # Change this rate to the current rate


    i, goal, temp_data = 0, len(crossrates_rows), []
    while i < goal:
        if i != 0 and i != goal-1:
            cells = crossrates_rows[i].find_all('td')
            temp_data.append((cells[1].text, cells[2].text))
        i+=1

    data = {
        "USD": 15.42
    }
    # print("Value of each currency in MVR")
    for each in temp_data:
        new_value = mvr_to_dollar / float(each[1])
        if round(new_value, 2) > 0.1:
            data[each[0]] = round(new_value, 2)
        else:
            data[each[0]] = new_value
    # print(data)

    return data

if __name__ == "__main__":
    data = get_exchange_rates()
    print(data)
