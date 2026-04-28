#!/usr/bin/env python3
"""
Efficient experiment runner for planning algorithms.
Gathers data for report generation.
"""

import sys
from air_cargo_problems import air_cargo_p1, air_cargo_p2, air_cargo_p3
from aimacode.search import breadth_first_search, depth_first_graph_search, uniform_cost_search
from aimacode.search import astar_search, greedy_best_first_graph_search
from my_planning_graph import PlanningGraph
import time

def h_pg_levelsum(node):
    return PlanningGraph(node.state, node.state.pos, serialize=True, ignore_mutexes=False).h_levelsum()

def h_pg_maxlevel(node):
    return PlanningGraph(node.state, node.state.pos, serialize=True, ignore_mutexes=False).h_maxlevel()

def h_pg_setlevel(node):
    return PlanningGraph(node.state, node.state.pos, serialize=True, ignore_mutexes=False).h_setlevel()

def h_unmet_goals(node):
    return len(node.state.goal - node.state.pos)

def run_experiment(problem, search_func, heuristic=None, name=""):
    """Run a single experiment and return metrics."""
    print(f"  Running {name}...", end="", flush=True)
    start_time = time.time()
    
    try:
        if heuristic:
            result = search_func(problem, h=heuristic)
        else:
            result = search_func(problem)
        
        elapsed = time.time() - start_time
        
        if result[0]:  # Found solution
            plan_len = len(result[0])
            expansions = result[1] if len(result) > 1 else 0
            print(f" OK ({plan_len} actions, {expansions} expansions, {elapsed:.3f}s)")
            return {
                'success': True,
                'plan_length': plan_len,
                'expansions': expansions,
                'time': elapsed
            }
        else:
            print(f" FAILED (no solution)")
            return {'success': False, 'time': elapsed}
    except Exception as e:
        elapsed = time.time() - start_time
        print(f" ERROR ({elapsed:.3f}s): {str(e)[:50]}")
        return {'success': False, 'time': elapsed, 'error': str(e)[:50]}

# Problem definitions
problems = [
    (air_cargo_p1, "Problem 1"),
    (air_cargo_p2, "Problem 2"),
    (air_cargo_p3, "Problem 3"),
]

# Algorithm definitions: (search_function, heuristic, name)
uninformed = [
    (breadth_first_search, None, "Breadth-First Search"),
    (depth_first_graph_search, None, "Depth-First Graph Search"),
    (uniform_cost_search, None, "Uniform Cost Search"),
]

informed = [
    (greedy_best_first_graph_search, h_unmet_goals, "Greedy BFS (h_unmet_goals)"),
    (greedy_best_first_graph_search, h_pg_levelsum, "Greedy BFS (h_levelsum)"),
    (greedy_best_first_graph_search, h_pg_maxlevel, "Greedy BFS (h_maxlevel)"),
    (astar_search, h_unmet_goals, "A* (h_unmet_goals)"),
    (astar_search, h_pg_levelsum, "A* (h_levelsum)"),
    (astar_search, h_pg_maxlevel, "A* (h_maxlevel)"),
]

# Run experiments
all_results = {}
for problem_func, problem_name in problems[:2]:  # Problems 1 and 2: all algorithms
    print(f"\n=== {problem_name} ===")
    problem = problem_func()
    all_results[problem_name] = {}
    
    # Uninformed
    for search_func, heur, name in uninformed:
        result = run_experiment(problem, search_func, heur, name)
        all_results[problem_name][name] = result
    
    # Informed
    for search_func, heur, name in informed:
        result = run_experiment(problem, search_func, heur, name)
        all_results[problem_name][name] = result

# Problems 3+: subset of algorithms
for problem_func, problem_name in problems[2:3]:  # Problem 3
    print(f"\n=== {problem_name} (Subset) ===")
    problem = problem_func()
    all_results[problem_name] = {}
    
    # One uninformed
    result = run_experiment(problem, breadth_first_search, None, "Breadth-First Search")
    all_results[problem_name]["Breadth-First Search"] = result
    
    # Two greedy heuristics
    result = run_experiment(problem, greedy_best_first_graph_search, h_pg_maxlevel, "Greedy BFS (h_maxlevel)")
    all_results[problem_name]["Greedy BFS (h_maxlevel)"] = result
    
    result = run_experiment(problem, greedy_best_first_graph_search, h_pg_levelsum, "Greedy BFS (h_levelsum)")
    all_results[problem_name]["Greedy BFS (h_levelsum)"] = result
    
    # Two A* heuristics
    result = run_experiment(problem, astar_search, h_pg_maxlevel, "A* (h_maxlevel)")
    all_results[problem_name]["A* (h_maxlevel)"] = result
    
    result = run_experiment(problem, astar_search, h_pg_levelsum, "A* (h_levelsum)")
    all_results[problem_name]["A* (h_levelsum)"] = result

print("\n\n=== SUMMARY ===")
for problem_name in all_results:
    print(f"\n{problem_name}:")
    for algo_name in all_results[problem_name]:
        result = all_results[problem_name][algo_name]
        if result.get('success'):
            print(f"  {algo_name:40s}: Plan={result['plan_length']}, Expansions={result['expansions']}, Time={result['time']:.3f}s")
        else:
            print(f"  {algo_name:40s}: FAILED ({result.get('error', 'timeout')})")

print("\nExperiments completed!")
