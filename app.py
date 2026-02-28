import numpy as np
import random
import math

class Team:

    def __init__(self, name):
        self.name = name

        # Capital
        self.cash = 100_000_000

        # Creative baseline
        self.quality = 0.7
        self.originality = 0.7
        self.audience_fit = 0.6
        self.technical = 0.75

        # Fame & algorithm state
        self.fame = 0.0
        self.trust = 0.2
        self.sentiment = 0.5

        self.subscribers = 0
        self.brand_equity = 0.0

        # Investment buckets
        self.production = 0
        self.marketing = 0
        self.mentor = False

    # ----------------------------------------
    # Capital allocation
    # ----------------------------------------

    def allocate(self, production, marketing, mentor=False):

        total = production + marketing
        if total > self.cash:
            raise ValueError("Not enough capital")

        self.cash -= total

        self.production = production
        self.marketing = marketing
        self.mentor = mentor

        # Effects
        self.technical += 0.05 * math.sqrt(production / 10_000_000)
        self.quality += 0.05 * math.sqrt(production / 10_000_000)

        if mentor:
            self.quality += 0.05
            self.originality -= 0.05

    # ----------------------------------------
    # Expected metrics
    # ----------------------------------------

    def expected_ctr(self):
        return 0.03 + 0.04 * self.originality + 0.02 * self.fame

    def expected_watch(self):
        return 0.3 + 0.5 * self.quality

    def expected_impressions(self):
        base = 2000 + 8000 * self.trust
        marketing_boost = 2000 * math.log1p(self.marketing / 10_000_000)
        return base + marketing_boost

    # ----------------------------------------
    # Daily simulation
    # ----------------------------------------

    def simulate_day(self, market_attention):

        exp_impr = min(self.expected_impressions(), market_attention)

        exp_ctr = self.expected_ctr()
        exp_watch = self.expected_watch()

        impressions = np.random.normal(exp_impr, exp_impr * 0.1)
        ctr = np.random.normal(exp_ctr, 0.005)
        watch = np.random.normal(exp_watch, 0.05)

        impressions = max(500, impressions)
        ctr = max(0.01, min(0.15, ctr))
        watch = max(0.1, min(0.9, watch))

        views = impressions * ctr

        performance = (ctr * watch) / (exp_ctr * exp_watch)

        self.trust += 0.05 * (performance - 1)
        self.trust = max(0.05, min(1.0, self.trust))

        if performance > 1.1:
            self.fame += 0.01 * performance

        revenue = views * 500
        self.cash += revenue

        new_subs = views * 0.01 * self.sentiment
        self.subscribers += new_subs

        self.brand_equity += 0.01 * (self.fame + self.sentiment)

        return views, revenue


# ----------------------------------------
# MARKET SIMULATION
# ----------------------------------------

def run_market(days=60):

    teams = [
        Team("Team A"),
        Team("Team B")
    ]

    # Allocate differently
    teams[0].allocate(40_000_000, 30_000_000, mentor=True)
    teams[1].allocate(20_000_000, 50_000_000, mentor=False)

    market_attention = 50_000

    for day in range(days):

        for team in teams:
            views, revenue = team.simulate_day(market_attention)

        # attention limited pool
        market_attention = 50_000 + random.randint(-5000, 5000)

    return teams


# ----------------------------------------
# RUN
# ----------------------------------------

teams = run_market()

for t in teams:
    print(t.name)
    print("Cash:", f"{int(t.cash):,} VND")
    print("Subscribers:", int(t.subscribers))
    print("Fame:", round(t.fame, 3))
    print("Trust:", round(t.trust, 3))
    print("-" * 30)
