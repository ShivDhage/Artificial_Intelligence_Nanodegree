"""
Report data generation and analysis for Planning algorithms
"""

# Experimental Results Summary
# Data extracted from test runs

results = {
    "Problem 1": {
        "actions": 20,
        "data": [
            {"algorithm": "Breadth-First Search", "expansions": 43, "plan_length": 6, "time": 0.00222},
            {"algorithm": "Depth-First Graph Search", "expansions": 21, "plan_length": 20, "time": 0.00124},
            {"algorithm": "Uniform Cost Search", "expansions": 60, "plan_length": 6, "time": 0.00344},
            {"algorithm": "Greedy BFS (h_unmet_goals)", "expansions": 7, "plan_length": 6, "time": 0.00062},
            {"algorithm": "Greedy BFS (h_pg_levelsum)", "expansions": 6, "plan_length": 6, "time": 0.08852},
            {"algorithm": "Greedy BFS (h_pg_maxlevel)", "expansions": 6, "plan_length": 6, "time": 0.05780},
        ]
    },
    "Problem 2": {
        "actions": 72,
        "data": [
            {"algorithm": "Breadth-First Search", "expansions": 3343, "plan_length": 9, "time": 0.68034},
            {"algorithm": "Depth-First Graph Search", "expansions": 624, "plan_length": 619, "time": 0.92630},
            {"algorithm": "Uniform Cost Search", "expansions": 5154, "plan_length": 9, "time": 1.16314},
            {"algorithm": "Greedy BFS (h_unmet_goals)", "expansions": 17, "plan_length": 9, "time": 0.00675},
            {"algorithm": "Greedy BFS (h_pg_levelsum)", "expansions": 9, "plan_length": 9, "time": 1.77814},
            {"algorithm": "Greedy BFS (h_pg_maxlevel)", "expansions": 27, "plan_length": 9, "time": 3.06863},
        ]
    }
}

# Analysis and insights
def analyze():
    print("=" * 80)
    print("PLANNING ALGORITHMS ANALYSIS")
    print("=" * 80)
    
    for problem_name, problem_data in results.items():
        print(f"\n{problem_name} ({problem_data['actions']} actions)")
        print("-" * 80)
        print(f"{'Algorithm':<35} {'Expansions':>12} {'Plan':<6} {'Time (s)':>12}")
        print("-" * 80)
        
        for entry in problem_data['data']:
            print(f"{entry['algorithm']:<35} {entry['expansions']:>12,} {entry['plan_length']:>5} {entry['time']:>12.4f}")
    
    print("\n" + "=" * 80)
    print("KEY OBSERVATIONS")
    print("=" * 80)
    
    # Observations about Problem 1
    p1_data = results["Problem 1"]["data"]
    best_uninformed_p1 = min(p1_data[:3], key=lambda x: x["expansions"])
    best_informed_p1 = min(p1_data[3:], key=lambda x: x["expansions"])
    
    print(f"\nProblem 1 (Small domain - 20 actions):")
    print(f"  - Best uninformed: {best_uninformed_p1['algorithm']} ({best_uninformed_p1['expansions']} expansions)")
    print(f"  - Best informed: {best_informed_p1['algorithm']} ({best_informed_p1['expansions']} expansions)")
    print(f"  - All algorithms find optimal plan (length 6)")
    print(f"  - Uninformed searches are practical and fast")
    
    # Observations about Problem 2
    p2_data = results["Problem 2"]["data"]
    best_uninformed_p2 = min(p2_data[:3], key=lambda x: x["expansions"])
    best_informed_p2 = min(p2_data[3:], key=lambda x: x["expansions"])
    
    print(f"\nProblem 2 (Medium domain - 72 actions):")
    print(f"  - Best uninformed: {best_uninformed_p2['algorithm']} ({best_uninformed_p2['expansions']} expansions)")
    print(f"  - Best informed: {best_informed_p2['algorithm']} ({best_informed_p2['expansions']} expansions)")
    print(f"  - Expansion ratio: {best_uninformed_p2['expansions'] / best_informed_p2['expansions']:.1f}x")
    print(f"  - Time ratio uninformed/informed: {best_uninformed_p2['time'] / best_informed_p2['time']:.1f}x")
    print(f"  - Depth-first returns suboptimal plan (619 vs optimal 9)")
    
    # Heuristic comparison
    print(f"\nHeuristic Quality Analysis (Problem 2):")
    print(f"  - h_unmet_goals: Simple but very effective (17 expansions)")
    print(f"  - h_pg_levelsum: Strong but computationally expensive (1.78s)")
    print(f"  - h_pg_maxlevel: Moderately effective but slower (3.07s)")
    print(f"  - Note: h_pg_setlevel was too slow to complete in reasonable time")

if __name__ == "__main__":
    analyze()
