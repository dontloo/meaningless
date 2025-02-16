import math

A4_FREQ = 440.0
JUST_INTERVALS = [
    (1, 1),     # Unison (0 semitones)
    (16, 15),   # Minor second (1 semitone)
    (9, 8),     # Major second (2 semitones)
    (6, 5),     # Minor third (3 semitones)
    (5, 4),     # Major third (4 semitones)
    (4, 3),     # Perfect fourth (5 semitones)
    (45, 32),   # Augmented fourth (6 semitones)
    (3, 2),     # Perfect fifth (7 semitones)
    (8, 5),     # Minor sixth (8 semitones)
    (5, 3),     # Major sixth (9 semitones)
    (16, 9),    # Minor seventh (10 semitones)
    (15, 8)     # Major seventh (11 semitones)
]

def get_just_ratio_and_freq(semitone_diff):
    if semitone_diff == 0:
        return "1/1", A4_FREQ
    
    is_above = semitone_diff > 0
    abs_diff = abs(semitone_diff)
    octaves, interval = divmod(abs_diff, 12)
    
    base_num, base_den = JUST_INTERVALS[interval]
    
    if is_above:
        numerator = base_num * (2 ** octaves)
        denominator = base_den
    else:
        numerator = base_den
        denominator = base_num * (2 ** octaves)
    
    # Simplify the ratio
    gcd_val = math.gcd(numerator, denominator)
    simple_num = numerator // gcd_val
    simple_den = denominator // gcd_val
    
    # Calculate frequency
    just_freq = A4_FREQ * (simple_num / simple_den)
    ratio_str = f"{simple_num}/{simple_den}"
    
    return ratio_str, just_freq

# Generate comparison table
print(f"{'Key':4} | {'12-TET (Hz)':12} | {'Just Ratio':10} | {'Just (Hz)':12} | {'Cents Diff':10}")
print("-" * 65)

for key in range(1, 89):
    semitone_diff = key - 49  # A4 is key 49
    et_freq = A4_FREQ * (2 ** (semitone_diff / 12))
    ratio, just_freq = get_just_ratio_and_freq(semitone_diff)
    
    # Calculate cents difference between ET and Just
    cents_diff = 1200 * math.log2(et_freq/just_freq) if et_freq != just_freq else 0
    
    print(f"{key:4} | {et_freq:12.2f} | {ratio:10} | {just_freq:12.2f} | {cents_diff:7.1f}¢")
