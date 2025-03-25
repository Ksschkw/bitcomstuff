from bs4 import BeautifulSoup
from collections import Counter
import random
import psycopg2

# Parse HTML and extract color data
html_content = """<html>
<head>
<title>Our Python Class exam</title>

<style type="text/css">
	
	body{
		width:1000px;
		margin: auto;
	}
	table,tr,td{
		border:solid;
		padding: 5px;
	}
	table{
		border-collapse: collapse;
		width:100%;
	}
	h3{
		font-size: 25px;
		color:green;
		text-align: center;
		margin-top: 100px;
	}
	p{
		font-size: 18px;
		font-weight: bold;
	}
</style>

</head>
<body>
<h3>TABLE SHOWING COLOURS OF DRESS BY WORKERS AT BINCOM ICT FOR THE WEEK</h3>
<table>
	
	<thead>
		<th>DAY</th><th>COLOURS</th>
	</thead>
	<tbody>
	<tr>
		<td>MONDAY</td>
		<td>GREEN, YELLOW, GREEN, BROWN, BLUE, PINK, BLUE, YELLOW, ORANGE, CREAM, ORANGE, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, GREEN</td>
	</tr>
	<tr>
		<td>TUESDAY</td>
		<td>ARSH, BROWN, GREEN, BROWN, BLUE, BLUE, BLEW, PINK, PINK, ORANGE, ORANGE, RED, WHITE, BLUE, WHITE, WHITE, BLUE, BLUE, BLUE</td>
	</tr>
	<tr>
		<td>WEDNESDAY</td>
		<td>GREEN, YELLOW, GREEN, BROWN, BLUE, PINK, RED, YELLOW, ORANGE, RED, ORANGE, RED, BLUE, BLUE, WHITE, BLUE, BLUE, WHITE, WHITE</td>
	</tr>
	<tr>
		<td>THURSDAY</td>
		<td>BLUE, BLUE, GREEN, WHITE, BLUE, BROWN, PINK, YELLOW, ORANGE, CREAM, ORANGE, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, GREEN</td>
	</tr>
	<tr>
		<td>FRIDAY</td>
		<td>GREEN, WHITE, GREEN, BROWN, BLUE, BLUE, BLACK, WHITE, ORANGE, RED, RED, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, WHITE</td>
	</tr>

	</tbody>
</table>

<p>Examine the sequence below very well, you will discover that for every 1s that appear 3 times, the output will be one, otherwise the output will be 0.</p>
<p>0101101011101011011101101000111 <span style="color:orange;">Input</span></p>
<p>0000000000100000000100000000001 <span style="color:orange;">Output</span></p>
<p>
</body>
</html>"""

soup = BeautifulSoup(html_content, 'html.parser')
table = soup.find('table')
rows = table.find_all('tr')[1:]  # Skip header

colors = []
for row in rows:
    cols = row.find_all('td')
    if len(cols) < 2:
        continue
    color_str = cols[1].text.strip()
    day_colors = [color.strip().upper() for color in color_str.split(', ')]
    colors.extend(day_colors)

color_counts = Counter(colors)
total_colors = len(colors)
unique_colors = len(color_counts)

# Question 1: Mean color (closest to mean frequency)
mean_freq = total_colors / unique_colors
closest_color = min(color_counts.items(), key=lambda x: abs(x[1] - mean_freq))[0]

# Question 2: Most frequent color
most_common = color_counts.most_common(1)[0][0]

# Question 3: Median color (sorted alphabetically)
sorted_colors = sorted(colors)
median_pos = (len(sorted_colors) - 1) // 2
median_color = sorted_colors[median_pos]

# Question 4: Variance of frequencies
freqs = list(color_counts.values())
mean_f = sum(freqs) / len(freqs)
variance = sum((f - mean_f) ** 2 for f in freqs) / len(freqs)

# Question 5: Probability of red
prob_red = color_counts.get('RED', 0) / total_colors

# Output results
print(f"1. Mean color: {closest_color}")
print(f"2. Most worn color: {most_common}")
print(f"3. Median color: {median_color}")
print(f"4. Variance: {variance:.2f}")
print(f"5. Probability of red: {prob_red:.4f}")

# Question 6: Save to PostgreSQL
'''
I do nto have postgreSQL installed so  i did not test this code to ee if it actually work, but it should, i used the method that i'd normally use with just sqlite3 in python
'''
def save_to_db():
    try:
        conn = psycopg2.connect(
            dbname="your_db",
            user="user",
            password="pass",
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS color_frequencies (
                color VARCHAR PRIMARY KEY,
                frequency INTEGER
            )
        """)
        for color, count in color_counts.items():
            cur.execute("""
                INSERT INTO color_frequencies (color, frequency)
                VALUES (%s, %s)
                ON CONFLICT (color) DO UPDATE SET frequency = EXCLUDED.frequency
            """, (color, count))
        conn.commit()
        print("6. Data saved to PostgreSQL.")
    except Exception as e:
        print(f"6. Database error: {e}")
    finally:
        if conn:
            conn.close()

save_to_db()

# Question 7: Recursive search
def recursive_search(arr, target, index=0):
    if index >= len(arr):
        return -1
    if arr[index] == target:
        return index
    return recursive_search(arr, target, index + 1)

# Example usage:
numbers = [2, 5, 3, 8, 9]
target = 8
print(f"7. Index of {target}: {recursive_search(numbers, target)}")

# Question 8: Generate binary number
binary = ''.join(random.choices('01', k=4))
decimal = int(binary, 2)
print(f"8. Binary: {binary}, Decimal: {decimal}")

# Question 9: Sum first 50 Fibonacci numbers
def sum_fibonacci(n):
    a, b, total = 0, 1, 0
    for _ in range(n):
        total += a
        a, b = b, a + b
    return total

print(f"9. Sum of first 50 Fibonacci numbers: {sum_fibonacci(50)}")