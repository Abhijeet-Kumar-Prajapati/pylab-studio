/* Multi Program - browser demos (JavaScript ports of the Python programs) */
(function () {
  "use strict";

  const OUT = [];
  const put = (s) => OUT.push(s);
  const fmt = (n) => (Number.isInteger(n) ? String(n) : parseFloat(n.toFixed(6)));

  function lines(v) {
    return v.split(/\r?\n/).map((x) => x.trim()).filter((x) => x !== "");
  }
  const nums = (v) => lines(v).map(Number);
  const isPrime = (n) => {
    if (!Number.isInteger(n) || n < 2) return false;
    for (let i = 2; i * i <= n; i++) if (n % i === 0) return false;
    return true;
  };
  const gcd = (a, b) => { a = Math.abs(a); b = Math.abs(b); while (b) { [a, b] = [b, a % b]; } return a; };
  const lcm = (a, b) => (gcd(a, b) === 0 ? 0 : Math.abs(a * b) / gcd(a, b));
  const ones = ["zero","one","two","three","four","five","six","seven","eight","nine","ten",
    "eleven","twelve","thirteen","fourteen","fifteen","sixteen","seventeen","eighteen","nineteen"];
  const tens = ["","","twenty","thirty","forty","fifty","sixty","seventy","eighty","ninety"];
  const shiftChar = (ch, k) => ch === ch.toLowerCase() && ch !== ch.toUpperCase()
    ? String.fromCharCode(97 + ((ch.charCodeAt(0) - 97 + k) % 26 + 26) % 26)
    : ch === ch.toUpperCase() && ch !== ch.toLowerCase()
      ? String.fromCharCode(65 + ((ch.charCodeAt(0) - 65 + k) % 26 + 26) % 26)
      : ch;

  const MIXED = ["calorie_estimate", "mad_libs", "rock_paper_scissors", "computer", "guess_number_game", "caesar_encrypt", "caesar_decrypt"];

  const QUOTES = [
    "Simplicity is the soul of efficiency. - Austin Freeman",
    "First, solve the problem. Then write the code. - John Johnson",
    "Experience is the name everyone gives to their mistakes. - Oscar Wilde",
    "Talk is cheap. Show me the code. - Linus Torvalds",
    "Stay hungry, stay foolish. - Steve Jobs",
    "Knowledge is power. - Francis Bacon",
    "Code is like humor. When you have to explain it, it is bad. - Cory House",
  ];
  const CHAT = {
    hello: ["Hi there!", "Hello!", "Greetings!"],
    hi: ["Hi there!", "Hello!", "Hey!"],
    name: ["I'm Computer AI.", "You can call me Computer."],
    help: ["Try: hello, how are you, name, or bye."],
    bye: ["Goodbye!", "See you!", "Bye!"],
  };
  const b64encode = (s) => btoa(unescape(encodeURIComponent(s)));
  const b64decode = (s) => decodeURIComponent(escape(atob(s.trim())));
  const under1000 = (v) => {
    const parts = [];
    if (v >= 100) { parts.push(ones[Math.floor(v / 100)] + " hundred"); v %= 100; }
    if (v >= 20) parts.push(tens[Math.floor(v / 10)] + (v % 10 ? " " + ones[v % 10] : ""));
    else if (v > 0) parts.push(ones[v]);
    return parts.join(" ") || "zero";
  };
  const rnd = (a, b) => Math.floor(Math.random() * (b - a + 1)) + a;

  const D = {
    /* ---------------- math ---------------- */
    add_two_numbers: (a) => put(`Result: ${fmt(a[0] + a[1])}`),
    subtract_two_numbers: (a) => put(`Result: ${fmt(a[0] - a[1])}`),
    multiply_two_numbers: (a) => put(`Result: ${fmt(a[0] * a[1])}`),
    divide_two_numbers: (a) => a[1] === 0 ? put("Error: cannot divide by zero.")
      : put(`Result: ${fmt(a[0] / a[1])}`),
    power: (a) => put(`Result: ${fmt(Math.pow(a[0], a[1]))}`),
    square_root: (a) => a[0] < 0 ? put("Error: square root of a negative number is not real.")
      : put(`sqrt(${fmt(a[0])}) = ${fmt(Math.sqrt(a[0]))}`),
    factorial: (a) => { const n = a[0]; if (n < 0 || n > 20) return put("Error: enter a number between 0 and 20.");
      let r = 1; for (let i = 2; i <= n; i++) r *= i; put(`${n}! = ${r}`); },
    prime_check: (a) => put(`${a[0]} is ${isPrime(a[0]) ? "PRIME" : "NOT prime"}`),
    fibonacci_n: (a) => { const n = a[0]; const s = []; let x = 0, y = 1;
      for (let i = 0; i < n; i++) { s.push(x); [x, y] = [y, x + y]; } put(s.join(" ") + " "); },
    gcd_two: (a) => put(`GCD(${a[0]}, ${a[1]}) = ${gcd(a[0], a[1])}`),
    lcm_two: (a) => put(`LCM(${a[0]}, ${a[1]}) = ${lcm(a[0], a[1])}`),
    average: (a) => put(`Average of ${a.length} numbers = ${fmt(a.reduce((s, x) => s + x, 0) / a.length)}`),
    minimum: (a) => put(`Minimum = ${fmt(Math.min(...a))}`),
    maximum: (a) => put(`Maximum = ${fmt(Math.max(...a))}`),
    percentage: (a) => a[1] === 0 ? put("Error: whole value cannot be zero.")
      : put(`${fmt(a[0])} is ${(a[0] / a[1] * 100).toFixed(2)}% of ${fmt(a[1])}`),
    area_circle: (a) => put(`Area = ${(Math.PI * a[0] * a[0]).toFixed(4)}`),
    area_rectangle: (a) => put(`Area = ${fmt(a[0] * a[1])}`),
    area_triangle: (a) => put(`Area = ${fmt(0.5 * a[0] * a[1])}`),
    perimeter_circle: (a) => put(`Circumference = ${(2 * Math.PI * a[0]).toFixed(4)}`),
    volume_cube: (a) => put(`Volume = ${fmt(a[0] ** 3)}`),
    volume_sphere: (a) => put(`Volume = ${(4 / 3 * Math.PI * a[0] ** 3).toFixed(4)}`),
    distance_formula: (a) => put(`Distance = ${fmt(Math.hypot(a[2] - a[0], a[3] - a[1]))}`),
    quadratic_solver: (a) => { const [A, B, C] = a; if (A === 0) return put("Error: a cannot be zero.");
      const d = B * B - 4 * A * C;
      const r1 = (-B + Math.sqrt(d)) / (2 * A); const r2 = (-B - Math.sqrt(d)) / (2 * A);
      put(`Roots: ${fmt(r1)} and ${fmt(r2)}`); },
    digit_sum: (a) => put("Digit sum = " + String(Math.abs(a[0])).split("").reduce((s, d) => s + (+d), 0)),
    armstrong: (a) => { const d = String(a[0]); const t = d.split("").reduce((s, x) => s + Math.pow(+x, d.length), 0);
      put(`${a[0]} is ${t === a[0] ? "an Armstrong number" : "not an Armstrong number"}`); },
    perfect_number: (a) => { const n = a[0]; let t = 0; for (let i = 1; i < n; i++) if (n % i === 0) t += i;
      put(`${n} is ${t === n ? "perfect" : "not perfect"}`); },
    strong_number: (a) => { const f = [1,1,2,6,24,120,720]; const n = a[0];
      const t = String(n).split("").reduce((s, d) => s + (f[+d] || 0), 0);
      put(`${n} is ${t === n ? "strong" : "not strong"}`); },
    harshad: (a) => { const n = a[0]; const s = String(n).split("").reduce((t, d) => t + (+d), 0);
      put(`${n} is ${s && n % s === 0 ? "a Harshad number" : "not a Harshad number"}`); },
    automorphic: (a) => put(`${a[0]} is ${String(a[0] * a[0]).endsWith(String(a[0])) ? "automorphic" : "not automorphic"}`),
    neon: (a) => { const n = a[0]; const s = String(n * n).split("").reduce((t, d) => t + (+d), 0);
      put(`${n} is ${s === n ? "a neon number" : "not a neon number"}`); },
    spy_number: (a) => { const d = String(a[0]).split("").map(Number);
      const p = d.reduce((s, x) => s * x, 1); const t = d.reduce((s, x) => s + x, 0);
      put(`${a[0]} is ${t === p ? "a spy number" : "not a spy number"}`); },
    tech_number: (a) => { const s = String(a[0]); const h = s.length >> 1;
      if (s.length % 2 || !h) return put(`${a[0]} is not a Tech number`);
      const t = (+s.slice(0, h)) + (+s.slice(h));
      put(`${a[0]} is ${t * t === a[0] ? "a Tech number" : "not a Tech number"}`); },
    divisors: (a) => { const n = a[0]; const d = []; for (let i = 1; i <= n; i++) if (n % i === 0) d.push(i);
      put("Divisors: [" + d.join(", ") + "]"); },
    factor_pairs: (a) => { const n = a[0]; const p = []; for (let i = 1; i <= n; i++) if (n % i === 0) p.push(`(${i}, ${n / i})`);
      put("Factor pairs: [" + p.join(", ") + "]"); },
    multiples: (a) => { const [n, c] = a; const m = []; for (let i = 1; i <= c; i++) m.push(n * i);
      put("Multiples: [" + m.join(", ") + "]"); },
    even_odd: (a) => put(`${a[0]} is ${a[0] % 2 === 0 ? "even" : "odd"}`),
    absolute: (a) => put(`|${fmt(a[0])}| = ${fmt(Math.abs(a[0]))}`),
    round_num: (a) => put(`${fmt(a[0])} rounded = ${Math.round(a[0])}`),
    floor: (a) => put(`floor(${fmt(a[0])}) = ${Math.floor(a[0])}`),
    ceil: (a) => put(`ceil(${fmt(a[0])}) = ${Math.ceil(a[0])}`),
    natural_log: (a) => a[0] <= 0 ? put("Error: log needs a positive number.")
      : put(`ln(${fmt(a[0])}) = ${fmt(Math.log(a[0]))}`),
    log10: (a) => a[0] <= 0 ? put("Error: log10 needs a positive number.")
      : put(`log10(${fmt(a[0])}) = ${fmt(Math.log10(a[0]))}`),
    exp: (a) => put(`exp(${fmt(a[0])}) = ${fmt(Math.exp(a[0]))}`),
    sin_deg: (a) => put(`sin(${fmt(a[0])} deg) = ${Math.sin(a[0] * Math.PI / 180).toFixed(6)}`),
    cos_deg: (a) => put(`cos(${fmt(a[0])} deg) = ${Math.cos(a[0] * Math.PI / 180).toFixed(6)}`),
    tan_deg: (a) => put(`tan(${fmt(a[0])} deg) = ${Math.tan(a[0] * Math.PI / 180).toFixed(6)}`),
    sum_natural: (a) => put(`Sum of 1..${a[0]} = ${(a[0] * (a[0] + 1)) / 2}`),
    sum_squares: (a) => put(`Sum of squares 1..${a[0]} = ${(a[0] * (a[0] + 1) * (2 * a[0] + 1)) / 6}`),
    sum_cubes: (a) => { const s = (a[0] * (a[0] + 1)) / 2; put(`Sum of cubes 1..${a[0]} = ${s * s}`); },
    multiplication_table: (a) => { const n = a[0]; for (let i = 1; i <= 10; i++) put(`${n} x ${String(i).padStart(2)} = ${n * i}`); },
    factorial_table: (a) => { const n = a[0]; if (n > 15) return put("Please enter 15 or less.");
      for (let i = 1; i <= n; i++) { let r = 1; for (let k = 2; k <= i; k++) r *= k; put(`${i}! = ${r}`); } },
    prime_list: (a) => { const p = []; for (let i = 2; i <= a[0]; i++) if (isPrime(i)) p.push(i);
      put("Primes: [" + p.join(", ") + "]"); },
    pyramid: (a) => { const n = a[0]; for (let i = 1; i <= n; i++)
      put(" ".repeat(n - i) + "*".repeat(2 * i - 1)); },
    diamond: (a) => { const n = a[0]; for (let i = 1; i <= n; i++) put(" ".repeat(n - i) + "*".repeat(2 * i - 1));
      for (let i = n - 1; i > 0; i--) put(" ".repeat(n - i) + "*".repeat(2 * i - 1)); },
    pascal_triangle: (a) => { let row = [1]; for (let i = 0; i < a[0]; i++) { put(row.join(" "));
      row = [1, ...row.slice(0, -1).map((v, k) => v + row[k + 1]), 1]; } },
    ascii_art: () => { put(""); put(" /\\_/\\"); put("( o.o )"); put(" > ^ <"); put(""); },

    /* ---------------- converters ---------------- */
    celsius_to_fahrenheit: (a) => put(`${fmt(a[0])} C = ${fmt(a[0] * 9 / 5 + 32)} F`),
    fahrenheit_to_celsius: (a) => put(`${fmt(a[0])} F = ${fmt((a[0] - 32) * 5 / 9)} C`),
    temperature_converter_plus: (a) => put(`${fmt(a[0])} C = ${fmt(a[0] * 9 / 5 + 32)} F = ${fmt(a[0] + 273.15)} K`),
    km_to_miles: (a) => put(`${fmt(a[0])} km = ${(a[0] * 0.621371).toFixed(4)} miles`),
    miles_to_km: (a) => put(`${fmt(a[0])} miles = ${(a[0] / 0.621371).toFixed(4)} km`),
    kg_to_pounds: (a) => put(`${fmt(a[0])} kg = ${(a[0] * 2.20462).toFixed(4)} lb`),
    pounds_to_kg: (a) => put(`${fmt(a[0])} lb = ${(a[0] / 2.20462).toFixed(4)} kg`),
    meters_to_feet: (a) => put(`${fmt(a[0])} m = ${(a[0] * 3.28084).toFixed(4)} ft`),
    feet_to_meters: (a) => put(`${fmt(a[0])} ft = ${(a[0] / 3.28084).toFixed(4)} m`),
    hours_to_minutes: (a) => put(`${fmt(a[0])} h = ${fmt(a[0] * 60)} minutes`),
    minutes_to_seconds: (a) => put(`${fmt(a[0])} min = ${fmt(a[0] * 60)} seconds`),
    binary_to_decimal: (a) => { const b = String(a[0]).replace(/\D/g, "");
      put(/^[01]+$/.test(b) ? `${b} in binary = ${parseInt(b, 2)} in decimal` : "Invalid binary number."); },
    decimal_to_binary: (a) => put(`${a[0]} in decimal = ${(a[0] >>> 0).toString(2)} in binary`),
    decimal_to_hex: (a) => put(`${a[0]} in decimal = ${(a[0] >>> 0).toString(16).toUpperCase()} in hex`),
    hex_to_decimal: (a) => { const h = String(a[0]).replace(/^0x/i, ""); const v = parseInt(h, 16);
      put(Number.isNaN(v) ? "Invalid hex number." : `${h} in hex = ${v} in decimal`); },
    number_to_words: (a) => { const n = a[0];
      if (n < 0 || n > 999999) return put("Please enter a number between 0 and 999999.");
      const thousands = under1000(Math.floor(n / 1000)); const rest = under1000(n % 1000);
      put(`${n} = ${(thousands + " thousand " + rest).trim()}`); },

    /* ---------------- strings ---------------- */
    reverse_string: (a) => put("Reversed: " + a[0].split("").reverse().join("")),
    palindrome_check: (a) => { const c = a[0].toLowerCase().replace(/[^a-z0-9]/g, "");
      put(`"${a[0]}" is ${c === c.split("").reverse().join("") ? "a palindrome" : "not a palindrome"}`); },
    word_count: (a) => put("Word count: " + a[0].split(/\s+/).filter(Boolean).length),
    char_count: (a) => put("Characters: " + a[0].length),
    uppercase: (a) => put("Uppercase: " + a[0].toUpperCase()),
    lowercase: (a) => put("Lowercase: " + a[0].toLowerCase()),
    title_case: (a) => put("Title case: " + a[0].replace(/\w\S*/g, (t) => t[0].toUpperCase() + t.slice(1).toLowerCase())),
    remove_spaces: (a) => put("Without spaces: " + a[0].replace(/\s/g, "")),
    count_vowels: (a) => put("Vowels: " + (a[0].toLowerCase().match(/[aeiou]/g) || []).length),
    sort_words: (a) => put("Sorted: " + a[0].split(/\s+/).filter(Boolean).sort().join(" ")),
    remove_duplicates: (a) => put("Unique: " + [...new Set(a[0].split(/\s+/).filter(Boolean))].join(" ")),
    caesar_encrypt: (a) => { const k = Number(a[1]) % 26;
      put("Encrypted: " + [...String(a[0])].map((c) => shiftChar(c, k)).join("")); },
    caesar_decrypt: (a) => { const k = Number(a[1]) % 26;
      put("Decrypted: " + [...String(a[0])].map((c) => shiftChar(c, -k)).join("")); },
    base64_encode: (a) => put("Base64: " + b64encode(a[0])),
    base64_decode: (a) => { try { put("Decoded: " + b64decode(a[0])); } catch (e) { put("Invalid Base64 input."); } },

    /* ---------------- finance ---------------- */
    simple_interest: (a) => { const [p, r, t] = a; const si = p * r * t / 100;
      put(`Simple interest = ${si.toFixed(2)}`); put(`Total amount = ${(p + si).toFixed(2)}`); },
    compound_interest: (a) => { const [p, r, t, n] = a;
      put(`Compound amount = ${(p * Math.pow(1 + r / (100 * n), n * t)).toFixed(2)}`); },
    compound_interest_plus: (a) => { const [p, r, t] = a;
      for (let y = 1; y <= t; y++) put(`Year ${y}: ${(p * Math.pow(1 + r / 100, y)).toFixed(2)}`); },
    emi: (a) => { const [p, r, n] = a; const rate = r / 1200;
      const e = rate ? p * rate * Math.pow(1 + rate, n) / (Math.pow(1 + rate, n) - 1) : p / n;
      put(`Monthly EMI = ${e.toFixed(2)}`); put(`Total payment = ${(e * n).toFixed(2)}`); },
    loan_emi: (a) => { const [p, r, n] = a; const rate = r / 1200;
      const e = rate ? p * rate * Math.pow(1 + rate, n) / (Math.pow(1 + rate, n) - 1) : p / n;
      put(`EMI = ${e.toFixed(2)}`); put(`Total interest = ${(e * n - p).toFixed(2)}`); },
    discount: (a) => { const [p, d] = a; const f = p * (1 - d / 100);
      put(`Final price = ${f.toFixed(2)}`); put(`You save = ${(p - f).toFixed(2)}`); },
    profit_loss: (a) => { const [cp, sp] = a; if (cp === 0) return put("Cost price cannot be zero.");
      const diff = sp - cp; const pct = diff / cp * 100;
      put(`${diff >= 0 ? "Profit" : "Loss"}: ${Math.abs(diff).toFixed(2)} (${Math.abs(pct).toFixed(2)}%)`); },
    tax: (a) => { const [amt, t] = a; const tax = amt * t / 100;
      put(`Tax = ${tax.toFixed(2)}`); put(`Total = ${(amt + tax).toFixed(2)}`); },

    /* ---------------- health ---------------- */
    bmi_calculator: (a) => { const [w, h] = a; if (h <= 0) return put("Height must be greater than zero.");
      const b = w / (h * h); const cat = b < 18.5 ? "Underweight" : b < 25 ? "Normal" : b < 30 ? "Overweight" : "Obese";
      put(`BMI = ${b.toFixed(2)} (${cat})`); },
    water_intake: (a) => put(`Recommended water: ${Math.round(a[0] * 35)} ml per day`),
    heart_rate_zones: (a) => { const m = 220 - a[0];
      put(`Maximum heart rate: ${m} bpm`);
      put(`Moderate zone: ${Math.round(m * 0.5)} - ${Math.round(m * 0.7)} bpm`);
      put(`Vigorous zone: ${Math.round(m * 0.7)} - ${Math.round(m * 0.85)} bpm`); },
    calorie_estimate: (a) => { const [w, h, age, g] = a;
      const bmr = 10 * w + 6.25 * h - 5 * age + (String(g).toLowerCase().startsWith("m") ? 5 : -161);
      put(`Estimated BMR = ${Math.round(bmr)} kcal/day`); },

    /* ---------------- games ---------------- */
    coin_toss: (a) => { const n = a[0] || 10; const r = []; for (let i = 0; i < n; i++) r.push(Math.random() < .5 ? "Heads" : "Tails");
      put("Results: [" + r.join(", ") + "]");
      put(`Heads: ${r.filter((x) => x === "Heads").length}  Tails: ${r.filter((x) => x === "Tails").length}`); },
    coin_flip_game: () => put("Result: " + (Math.random() < .5 ? "Heads" : "Tails")),
    dice_roll: (a) => { const n = a[0] || 2; const r = []; for (let i = 0; i < n; i++) r.push(rnd(1, 6));
      put("Rolls: [" + r.join(", ") + "]"); put(`Total: ${r.reduce((s, x) => s + x, 0)}`); },
    dice_roller: (a) => { const [s, c] = a; const r = []; for (let i = 0; i < c; i++) r.push(rnd(1, s));
      put("Rolls: [" + r.join(", ") + "]"); put(`Total: ${r.reduce((t, x) => t + x, 0)}`); },
    rock_paper_scissors: (a) => { const pick = ["rock", "paper", "scissors"];
      const user = String(a[0] || "").toLowerCase(); const comp = pick[rnd(0, 2)];
      put(`Computer chose: ${comp}`);
      if (!pick.includes(user)) return put("Invalid choice.");
      const beats = { rock: "scissors", paper: "rock", scissors: "paper" };
      put(user === comp ? "Draw!" : beats[user] === comp ? "You win!" : "You lose!"); },
    guess_number_game: (a) => { const target = rnd(1, 100);
      let out = `I picked a number between 1 and 100. You typed: ${a[0] || "(nothing)"}\n`;
      out += Math.abs((a[0] || 50) - target) <= 3 ? "Very close!" : (a[0] || 50) < target ? "Too low." : "Too high.";
      put(out); },
    mad_libs: (a) => put(`The ${a[2]} ${a[0]} likes to ${a[1]} every single day.`),

    /* ---------------- utility ---------------- */
    password_generator: (a) => { const len = a[0] || 12; const count = a[1] || 5;
      const pool = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()-_=+";
      for (let i = 0; i < count; i++) { let s = ""; for (let j = 0; j < len; j++) s += pool[rnd(0, pool.length - 1)]; put(s); } },
    random_password_plus: (a) => { const len = a[0] || 12;
      const pool = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%";
      let s = ""; for (let j = 0; j < len; j++) s += pool[rnd(0, pool.length - 1)];
      put("Password: " + s); },
    random_number: (a) => { let lo = a[0], hi = a[1]; if (lo > hi) [lo, hi] = [hi, lo];
      put("Random number: " + rnd(lo, hi)); },
    random_string: (a) => { const n = a[0] || 8; const pool = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
      let s = ""; for (let i = 0; i < n; i++) s += pool[rnd(0, pool.length - 1)];
      put("Random string: " + s); },
    countdown_timer: (a) => { const s = a[0] || 10;
      put(`Countdown from ${s}:`); for (let i = s; i > 0; i--) put(String(i).padStart(4) + "s"); put("Time is up!"); },
    stopwatch: (a) => put(`A ${a[0] || 10} second stopwatch would run here. In the browser this one is live.`),
    quote_generator: (a) => { const n = Math.min(a[0] || 3, QUOTES.length);
      const pool = [...QUOTES]; for (let i = 0; i < n; i++) put(" - " + pool.splice(rnd(0, pool.length - 1), 1)[0]); },
    tip_calculator: (a) => { const [bill, tip, people] = a; const t = bill * tip / 100; const total = bill + t;
      put(`Tip: ${t.toFixed(2)}`); put(`Total: ${total.toFixed(2)}`);
      put(`Per person: ${(total / Math.max(people || 1, 1)).toFixed(2)}`); },
    age_calculator: (a) => { const [y, m, d] = a; const now = new Date();
      let age = now.getFullYear() - y;
      if (now.getMonth() + 1 < m || (now.getMonth() + 1 === m && now.getDate() < d)) age--;
      put(`Age: ${age} years`); },
    leap_year: (a) => { const y = a[0]; const l = (y % 4 === 0 && y % 100 !== 0) || y % 400 === 0;
      put(`${y} is ${l ? "a leap year" : "not a leap year"}`); },
    day_of_week: (a) => { const [y, m, d] = a;
      put("Weekday: " + new Date(y, m - 1, d).toLocaleDateString(undefined, { weekday: "long" })); },
    days_between: (a) => { const [s, e] = a; const d1 = new Date(s), d2 = new Date(e);
      if (isNaN(d1) || isNaN(d2)) return put("Invalid date. Use YYYY-MM-DD.");
      put("Days between: " + Math.abs((d2 - d1) / 86400000 | 0)); },
    system_info: () => { put("Browser: " + navigator.userAgent.split(") ")[0] + ")");
      put("Platform: " + navigator.platform); put("Language: " + navigator.language);
      put("Screen: " + screen.width + "x" + screen.height); },
    current_time: () => { const n = new Date();
      put("Date: " + n.toISOString().slice(0, 10));
      put("Time: " + n.toTimeString().slice(0, 8)); },
    timestamp: () => put("Unix timestamp: " + Math.floor(Date.now() / 1000)),
    computer: (a) => { const t = String(a[0] || "").toLowerCase();
      for (const key of Object.keys(CHAT)) if (t.includes(key)) { put("Computer: " + CHAT[key][rnd(0, CHAT[key].length - 1)]); return; }
      put("Computer: I'm not sure how to respond to that."); },
  };

  const SAMPLES = {
    add_two_numbers: "5\n3", area_circle: "5", quadratic_solver: "1\n-5\n6",
    guess_number_game: "50", rock_paper_scissors: "rock", caesar_encrypt: "hello world\n3",
    caesar_decrypt: "khoor fruzg\n3", emi: "500000\n8\n240", compound_interest: "1000\n10\n2\n4",
    compound_interest_plus: "1000\n10\n3", simple_interest: "1000\n5\n2", loan_emi: "500000\n8\n240",
    discount: "1000\n20", profit_loss: "100\n120", tax: "1000\n10", base64_encode: "hello world",
    base64_decode: "aGVsbG8gd29ybGQ=", number_to_words: "999", palindrome_check: "level",
    reverse_string: "hello", sort_words: "banana apple cherry", remove_duplicates: "a b a c b",
    count_vowels: "education", title_case: "hello world", seconds_test: "", minutes_to_seconds: "5",
    hours_to_minutes: "2", day_of_week: "2024\n1\n1", strong_number: "145", password_generator: "12\n3",
    computer: "hello", mad_libs: "dog\nrun\nfast", calorie_estimate: "70\n175\n30\nm",
    tip_calculator: "1000\n15\n2", age_calculator: "2005\n6\n15", days_between: "2024-01-01\n2024-12-31",
    binary_to_decimal: "1010", hex_to_decimal: "ff", decimal_to_hex: "255", number_to_words: "123",
    countdown_timer: "10", dice_roller: "6\n2", coin_toss: "5", timer: "10",
    minecraft: "", list_directory: ".", ascii_art: "", current_time: "", system_info: "",
    timestamp: "", random_number: "1\n100", random_string: "8", random_password_plus: "12",
    password_generator: "12\n3", stopwatch: "10", quote_generator: "3",
    heart_rate_zones: "30", water_intake: "70", bmi_calculator: "70\n1.75",
    muscle: "", random: "", matrix: "", stack: "", linked_list: "", queue: "", tree: "",
  };

  window.MP = {
    has: (slug) => Object.prototype.hasOwnProperty.call(D, slug),
    sample: (slug) => SAMPLES[slug] || "",
    list: () => Object.keys(D),
    run: function (slug, input) {
      const fn = D[slug];
      if (!fn) return ["This program is available in the Python version only."];
      OUT.length = 0;
      const raw = lines(input || "");
      if (!raw.length) return ["Please enter at least one value."];
      const text = raw.filter((x) => isNaN(Number(x)));
      const numbers = raw.map(Number);
      const mixed = MIXED.indexOf(slug) !== -1;
      try {
        if (mixed) fn(raw);
        else if (raw.every((x) => !isNaN(Number(x)))) fn(numbers);
        else fn(text);
      } catch (e) {
        OUT.push("Error: " + e.message);
      }
      return OUT.length ? OUT : ["(no output)"];
    },
  };
})();