#!/bin/python3

import os
import heapq


def shortestPath(a, queries):
    rows = len(a)
    cols = len(a[0])

    INF = 10**30
    answer = [INF] * len(queries)

    def solve(left, right, query_ids):
        if not query_ids or left > right:
            return

        # If only one column remains
        if left == right:
            for qi in query_ids:
                r1, c1, r2, c2 = queries[qi]

                start = min(r1, r2)
                end = max(r1, r2)

                cost = 0
                for r in range(start, end + 1):
                    cost += a[r][left]

                answer[qi] = min(answer[qi], cost)

            return

        mid = (left + right) // 2
        width = right - left + 1

        # Run Dijkstra from every cell in the middle column
        for source_row in range(rows):

            dist = [INF] * (rows * width)

            source = source_row * width + (mid - left)
            dist[source] = a[source_row][mid]

            pq = [(a[source_row][mid], source)]

            while pq:
                current_dist, u = heapq.heappop(pq)

                if current_dist != dist[u]:
                    continue

                r = u // width
                c = u % width

                # Up
                if r > 0:
                    v = u - width
                    nr = r - 1
                    nc = c
                    new_dist = current_dist + a[nr][left + nc]

                    if new_dist < dist[v]:
                        dist[v] = new_dist
                        heapq.heappush(pq, (new_dist, v))

                # Down
                if r + 1 < rows:
                    v = u + width
                    nr = r + 1
                    nc = c
                    new_dist = current_dist + a[nr][left + nc]

                    if new_dist < dist[v]:
                        dist[v] = new_dist
                        heapq.heappush(pq, (new_dist, v))

                # Left
                if c > 0:
                    v = u - 1
                    nr = r
                    nc = c - 1
                    new_dist = current_dist + a[nr][left + nc]

                    if new_dist < dist[v]:
                        dist[v] = new_dist
                        heapq.heappush(pq, (new_dist, v))

                # Right
                if c + 1 < width:
                    v = u + 1
                    nr = r
                    nc = c + 1
                    new_dist = current_dist + a[nr][left + nc]

                    if new_dist < dist[v]:
                        dist[v] = new_dist
                        heapq.heappush(pq, (new_dist, v))

            # Update answers for queries whose path can cross
            # the middle column
            for qi in query_ids:
                r1, c1, r2, c2 = queries[qi]

                p1 = r1 * width + (c1 - left)
                p2 = r2 * width + (c2 - left)

                if dist[p1] < INF and dist[p2] < INF:
                    candidate = (
                        dist[p1]
                        + dist[p2]
                        - a[source_row][mid]
                    )

                    if candidate < answer[qi]:
                        answer[qi] = candidate

        # Queries completely on the left
        left_queries = []

        # Queries completely on the right
        right_queries = []

        for qi in query_ids:
            r1, c1, r2, c2 = queries[qi]

            if c1 < mid and c2 < mid:
                left_queries.append(qi)

            elif c1 > mid and c2 > mid:
                right_queries.append(qi)

        solve(left, mid - 1, left_queries)
        solve(mid + 1, right, right_queries)

    solve(0, cols - 1, list(range(len(queries))))

    return answer


if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    first_multiple_input = input().rstrip().split()

    n = int(first_multiple_input[0])
    m = int(first_multiple_input[1])

    a = []

    for _ in range(n):
        a.append(list(map(int, input().rstrip().split())))

    q = int(input().strip())

    queries = []

    for _ in range(q):
        queries.append(list(map(int, input().rstrip().split())))

    result = shortestPath(a, queries)

    fptr.write('\n'.join(map(str, result)))
    fptr.write('\n')

    fptr.close()
