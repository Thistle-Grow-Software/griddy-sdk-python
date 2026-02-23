# Pro Football Reference Boxscore Page — Link Category Summary

**Source Page:** [Pittsburgh Steelers at New England Patriots — September 10, 2015](https://www.pro-football-reference.com/boxscores/201509100nwe.htm)

This document categorizes the outbound links on the above PFR boxscore page that reference **other Pro Football Reference pages**. Excluded from this analysis are:

- **On-page anchor links** (the "On this page:" navigation that jumps to sections within the same boxscore)
- **"NFL Scores — Week 1" sidebar** (links to other games played during Week 1 of 2015)
- **Non-PFR external links** (Sports Reference sister sites, YouTube, social media, SportsLogos.net, etc.)

---

## 1. Player Profile Pages

**URL pattern:** `/players/{Letter}/{PlayerId}.htm`

**Example:** `https://www.pro-football-reference.com/players/B/BradTo00.htm` (Tom Brady)

**Description:** Each player who appeared in the game or is mentioned on the page links to their individual player profile. A player profile page on PFR typically contains career statistics (passing, rushing, receiving, defensive, etc.), a game log for each season, advanced stats, approximate value, combine data, contract/salary information, snap counts, fantasy stats, and similar/comparable players.

**Where these links appear on the boxscore page:**

- **Scoring summary** — every player involved in a scoring play (scorer, passer, kicker)
- **Passing, Rushing, & Receiving table** — every player with offensive stats
- **Defense table** — every player with defensive stats (tackles, sacks, interceptions)
- **Kick/Punt Returns table** — every returner
- **Kicking & Punting table** — every kicker and punter
- **Starting Lineups** — every offensive and defensive starter for both teams
- **Snap Counts** — every player who recorded any offensive, defensive, or special teams snaps
- **Full Play-by-Play** — every player mentioned in any play description (ball carrier, passer, receiver, tackler, penalty recipient, etc.)
- **Site-wide navigation/footer** — "Popular" and "In the News" player lists in the mega-menu

**Approximate count:** ~80+ unique player profiles linked, with hundreds of total link instances due to repetition across tables and the play-by-play log.

---

## 2. Team Season Pages

**URL pattern:** `/teams/{team_abbrev}/{year}.htm`

**Example:** `https://www.pro-football-reference.com/teams/nwe/2015.htm` (2015 New England Patriots)

**Description:** Links to a team's page for a specific season. These pages contain the team's full roster, schedule and results, team stats, starters, draft picks, salary cap info, and coaching staff for that year.

**Where these links appear on the boxscore page:**

- **Game header** — both the "Pittsburgh Steelers" and "New England Patriots" team names link to their respective 2015 season pages
- **Score line and quarter-by-quarter summary** — team abbreviations (PIT, NWE) link to 2015 season pages
- **Breadcrumb navigation** — "New England Patriots Schedule" and "Pittsburgh Steelers Schedule" at the top
- **Site-wide footer navigation** — all 32 current NFL teams link to their current (2025) season pages

---

## 3. Team Franchise Pages

**URL pattern:** `/teams/{team_abbrev}/`

**Example:** `https://www.pro-football-reference.com/teams/nwe/` (New England Patriots franchise history)

**Description:** The franchise-level page showing a team's complete historical record across all seasons, including year-by-year records, all-time leaders, coaching history, and draft history. In the site navigation, these are linked via the "F" (Franchise) icon next to each current team name.

**Where these links appear:** Site-wide mega-menu navigation alongside current team season links.

---

## 4. Coach Profile Pages

**URL pattern:** `/coaches/{CoachId}.htm`

**Example:** `https://www.pro-football-reference.com/coaches/BeliBi0.htm` (Bill Belichick)

**Description:** Links to a head coach's career page, which includes their win-loss record by season, career coaching tree, playoff history, and awards.

**Where these links appear:**

- **Game header** — "Coach: Mike Tomlin" and "Coach: Bill Belichick" directly under each team's name/logo
- **Site-wide footer navigation** — lists of active and historical coaches

---

## 5. Game Official Profile Pages

**URL pattern:** `/officials/{OfficialId}.htm`

**Example:** `https://www.pro-football-reference.com/officials/ChefCa0r.htm` (Carl Cheffers)

**Description:** Links to the profile page of each game official. Official pages typically show their career history of games officiated, penalty stats, and crew assignments.

**Where these links appear:** The "Officials" section of the boxscore, which lists the Referee, Umpire, Head Linesman, Line Judge, Back Judge, Side Judge, and Field Judge. Seven official links total for this game.

---

## 6. Stadium Pages

**URL pattern:** `/stadiums/{StadiumId}.htm`

**Example:** `https://www.pro-football-reference.com/stadiums/BOS00.htm` (Gillette Stadium)

**Description:** Links to a stadium's page showing its hosting history, attendance records, and notable games played there.

**Where these links appear:**

- **Game Info section** — "Gillette Stadium" in the game details
- **Site-wide footer navigation** — examples like Lambeau Field, Superdome, Candlestick Park

---

## 7. Season Overview Pages

**URL pattern:** `/years/{year}/` and `/years/{year}/{stat_category}.htm`

**Example:** `https://www.pro-football-reference.com/years/2015/` (2015 NFL season)

**Description:** Links to a season's main page (standings, team stats) or a specific statistical category page for that season (passing leaders, rushing leaders, draft results, etc.). Season pages provide league-wide standings, team rankings, and aggregate statistical summaries.

**Where these links appear:**

- **Breadcrumb/header navigation** — "2015 NFL Scores & Schedule"
- **Site-wide mega-menu** — links to recent seasons (2025, 2024, 2023, ...) each with sub-links to passing, rushing, receiving, defense, kicking, punting, returns, scoring, fantasy, draft, and leaders pages
- **Attendance link** — the attendance figure "66,829" links to the 2015 season attendance page (`/years/2015/attendance.htm`)

---

## 8. Next Game / Adjacent Boxscore Links

**URL pattern:** `/boxscores/{date}{team}.htm`

**Example:** `https://www.pro-football-reference.com/boxscores/201509200pit.htm` (Steelers' next game)

**Description:** Links to other individual game boxscores. In the game header area, each team has a "Next Game" link pointing to their following regular-season game's boxscore.

**Where these links appear:** Game header under each team — "Next Game" links.

---

## 9. Week Summary Pages

**URL pattern:** `/years/{year}/week_{number}.htm`

**Example:** `https://www.pro-football-reference.com/years/2015/week_1.htm`

**Description:** A page showing all games played during a specific week of the NFL season, with scores and links to each boxscore.

**Where these links appear:** The "NFL Scores — Week 1" header label links to the Week 1 summary page. *(Note: while the individual game links in that sidebar section were excluded per instructions, the "Week 1" header link itself is a navigational link to the week summary.)*

---

## 10. Boxscore Index / Scores Landing Pages

**URL pattern:** `/boxscores/` and related subpages

**Examples:**
- `https://www.pro-football-reference.com/boxscores/` (main scores index)
- `https://www.pro-football-reference.com/boxscores/game-scores.htm` (all-time scores)
- `https://www.pro-football-reference.com/boxscores/game_scores_find.cgi` (score finder tool)
- `https://www.pro-football-reference.com/boxscores/win_prob.cgi` (win probability calculator)
- `https://www.pro-football-reference.com/boxscores/standings.cgi` (historical standings)

**Description:** Various landing and tool pages for finding and browsing NFL game scores across history.

**Where these links appear:** Site-wide navigation menus and footer — "NFL Scores & Boxes", "All-time Scores", "Find a Score", etc.

---

## 11. Career Leaders Pages

**URL pattern:** `/leaders/{stat}_{scope}.htm`

**Examples:**
- `https://www.pro-football-reference.com/leaders/pass_yds_career.htm`
- `https://www.pro-football-reference.com/leaders/rush_td_single_season.htm`
- `https://www.pro-football-reference.com/leaders/sacks_single_game.htm`

**Description:** Statistical leaderboard pages showing career, single-season, single-game, active, or year-by-year leaders for various stat categories (passing yards, rushing TDs, receptions, all TDs, interceptions, etc.).

**Where these links appear:** The site-wide mega-menu "Leaders" section, which includes dozens of links organized by stat category and scope (Career, Single-Season, Single Game, Active, Year-by-Year).

---

## 12. NFL Draft Pages

**URL pattern:** `/years/{year}/draft.htm`, `/draft/{year}-combine.htm`, `/teams/{team}/draft.htm`, `/draft/`

**Examples:**
- `https://www.pro-football-reference.com/years/2025/draft.htm`
- `https://www.pro-football-reference.com/draft/2024-combine.htm`
- `https://www.pro-football-reference.com/teams/chi/draft.htm`

**Description:** Pages related to the NFL Draft — annual draft results, combine results, and team-specific draft histories.

**Where these links appear:** Site-wide mega-menu under "Draft" with year-by-year draft pages, combine pages, and team-specific draft history links.

---

## 13. Awards & Hall of Fame Pages

**URL pattern:** `/awards/`, `/hof/`, `/probowl/`

**Examples:**
- `https://www.pro-football-reference.com/hof/` (Hall of Fame)
- `https://www.pro-football-reference.com/awards/ap-nfl-mvp-award.htm` (AP NFL MVP)
- `https://www.pro-football-reference.com/probowl/` (Pro Bowl)

**Description:** Pages listing NFL award winners (MVP, Offensive/Defensive Player of the Year, etc.), Hall of Fame inductees, and Pro Bowl selections.

**Where these links appear:** Site-wide navigation — "Hall of Famers", "MVPs", "Pro Bowlers", "All Awards", and footer links.

---

## 14. Super Bowl Pages

**URL pattern:** `/super-bowl/`

**Examples:**
- `https://www.pro-football-reference.com/super-bowl/`
- `https://www.pro-football-reference.com/super-bowl/leaders.htm`
- `https://www.pro-football-reference.com/super-bowl/standings.htm`

**Description:** Pages covering Super Bowl history, including winners, leaders in Super Bowl stats, and franchise Super Bowl standings.

**Where these links appear:** Site-wide footer navigation.

---

## 15. Schools / Colleges Pages

**URL pattern:** `/schools/`

**Examples:**
- `https://www.pro-football-reference.com/schools/` (All Player Colleges)
- `https://www.pro-football-reference.com/schools/high_schools.cgi` (High Schools)

**Description:** Index pages listing the colleges and high schools that have produced NFL players.

**Where these links appear:** Site-wide footer navigation.

---

## 16. Executives Pages

**URL pattern:** `/executives/{ExecutiveId}.htm`

**Examples:**
- `https://www.pro-football-reference.com/executives/AdamBu0.htm` (Bud Adams)
- `https://www.pro-football-reference.com/executives/PiolSc0.htm` (Scott Pioli)

**Description:** Profile pages for NFL team executives (owners, general managers, etc.).

**Where these links appear:** Site-wide footer navigation.

---

## 17. Fantasy Football Pages

**URL pattern:** `/fantasy/`

**Examples:**
- `https://www.pro-football-reference.com/fantasy/`
- `https://www.pro-football-reference.com/fantasy/QB-fantasy-matchups.htm`
- `https://www.pro-football-reference.com/years/2025/fantasy-points-against-QB.htm`

**Description:** Fantasy football resources including matchup analysis and points-allowed rankings.

**Where these links appear:** Site-wide footer navigation.

---

## 18. Frivolities / Fun Tools Pages

**URL pattern:** `/friv/`

**Examples:**
- `https://www.pro-football-reference.com/friv/players-who-played-for-multiple-teams-franchises.fcgi`
- `https://www.pro-football-reference.com/friv/linkify.cgi` (Player Linker Tool)
- `https://www.pro-football-reference.com/friv/birthdays.cgi`
- `https://www.pro-football-reference.com/players/uniform.cgi` (Uniform Numbers)

**Description:** Novelty and utility pages — tools for finding players who played for multiple teams, linking player names in text, looking up birthdays, and browsing uniform number history.

**Where these links appear:** Site-wide footer navigation.

---

## 19. About / Glossary / Reference Pages

**URL pattern:** `/about/`

**Examples:**
- `https://www.pro-football-reference.com/about/glossary.htm`
- `https://www.pro-football-reference.com/about/minimums.htm`
- `https://www.pro-football-reference.com/about/nfl-football-faqs.html`
- `https://www.pro-football-reference.com/about/win_prob.htm`
- `https://www.pro-football-reference.com/about/sources.htm`

**Description:** Reference and informational pages — statistical glossaries, minimum qualification thresholds, FAQs about football, win probability methodology explanations, and data source attributions.

**Where these links appear:** Glossary links appear in each stat table's share/export toolbar; other about pages appear in the site footer.

---

## 20. Team Historical / Aggregate Pages

**URL pattern:** `/teams/comebacks.htm`, `/teams/`

**Examples:**
- `https://www.pro-football-reference.com/teams/comebacks.htm` (Biggest Comebacks)
- `https://www.pro-football-reference.com/teams/` (All Teams index)

**Description:** Aggregate team history pages like comeback records and the main index of all NFL/AFL franchise histories.

**Where these links appear:** Site-wide mega-menu navigation.

---

## 21. Player Index Pages

**URL pattern:** `/players/` and `/players/{stat_type}.htm`

**Examples:**
- `https://www.pro-football-reference.com/players/` (All Players index)
- `https://www.pro-football-reference.com/players/salary.htm` (2025 Salaries)
- `https://www.pro-football-reference.com/players/injuries.htm` (Current Injuries)

**Description:** Indexes and aggregate views of NFL players — browsable alphabetical player index, current salary data, and injury reports.

**Where these links appear:** Site-wide mega-menu navigation.

---

## 22. Blog & Newsletter Pages

**URL pattern:** `/pfr-blog/`, `/email/`, `/blog/`

**Examples:**
- `https://www.pro-football-reference.com/pfr-blog/`
- `https://www.pro-football-reference.com/email/`
- `https://www.pro-football-reference.com/blog/index37a8.html` (Approximate Value Formula)

**Description:** PFR blog articles, the email newsletter signup page, and specific blog posts explaining methodologies like the Approximate Value formula.

**Where these links appear:** Site footer.

---

## Summary Table

| # | Category | URL Pattern Example | Approx. Unique Links | Context |
|---|----------|-------------------|----------------------|---------|
| 1 | Player Profiles | `/players/B/BradTo00.htm` | ~80+ | Stats tables, play-by-play, lineups, snap counts |
| 2 | Team Season Pages | `/teams/nwe/2015.htm` | ~70 | Game header, nav (all 32 teams × current + 2015) |
| 3 | Team Franchise Pages | `/teams/nwe/` | ~32 | Navigation menu |
| 4 | Coach Profiles | `/coaches/BeliBi0.htm` | ~10 | Game header + nav |
| 5 | Official Profiles | `/officials/ChefCa0r.htm` | 7 | Officials section |
| 6 | Stadium Pages | `/stadiums/BOS00.htm` | ~4 | Game info + nav |
| 7 | Season Overview | `/years/2015/` | ~50+ | Breadcrumbs + nav (multi-year, multi-stat) |
| 8 | Adjacent Boxscores | `/boxscores/201509200pit.htm` | 2 | "Next Game" links |
| 9 | Week Summary | `/years/2015/week_1.htm` | 1 | Week header |
| 10 | Scores / Tools | `/boxscores/` | ~5 | Navigation |
| 11 | Career Leaders | `/leaders/pass_yds_career.htm` | ~30+ | Navigation mega-menu |
| 12 | NFL Draft | `/years/2025/draft.htm` | ~25 | Navigation mega-menu |
| 13 | Awards / HOF | `/hof/`, `/awards/` | ~5 | Navigation |
| 14 | Super Bowl | `/super-bowl/` | ~3 | Footer |
| 15 | Schools | `/schools/` | ~2 | Footer |
| 16 | Executives | `/executives/AdamBu0.htm` | ~4 | Footer |
| 17 | Fantasy Football | `/fantasy/` | ~3 | Footer |
| 18 | Frivolities | `/friv/` | ~4 | Footer |
| 19 | About / Glossary | `/about/glossary.htm` | ~6 | Table toolbars + footer |
| 20 | Team Aggregates | `/teams/comebacks.htm` | ~2 | Navigation |
| 21 | Player Index | `/players/salary.htm` | ~3 | Navigation |
| 22 | Blog / Newsletter | `/pfr-blog/`, `/email/` | ~3 | Footer |