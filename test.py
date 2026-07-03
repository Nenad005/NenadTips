from TeamMatcher import TeamMatcher

matcher = TeamMatcher()
m1home = "Novi Pazar"
m1away = "TSC"
m2home = "Novi Pazar"
m2away = "TSC Backa Topola"
m1time = "2025-02-24T16:30:00"
m2time = "2025-02-24T16:30:00"


print(matcher.match(m1home, m1away, m2home, m2away, m1time, m2time))