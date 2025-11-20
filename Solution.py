class PaymentRouter:
    def __init__(self, corridors):
        # Store corridors and build graph representation
        self.corridors = corridors
        self.graph = self.build_graph(corridors)

    def build_graph(self, corridors):
        """
        Builds a graph representation of the corridors for easy traversal.
        """
        graph = {}
        for src, dest, fee, rate in corridors:
            if src not in graph:
                graph[src] = []
            graph[src].append({"destination": dest, "fee": fee, "rate": rate})
        return graph

    def find_best_route(self, payment_request):
        """
        Finds the most cost-efficient route for the payment from source_currency to destination_currency.
        Uses a modified Dijkstra's algorithm to maximize the amount received at destination.

        The algorithm explores all possible routes and returns the one that maximizes
        the final amount received after all fees and currency conversions.

        payment_request: {
            "amount": float,
            "source_currency": str,
            "destination_currency": str
        }

        Returns: {
            "total_fee": float,
            "total_received": float
        }
        """
        import heapq

        source = payment_request["source_currency"]
        destination = payment_request["destination_currency"]
        amount = payment_request["amount"]

        # Priority queue: (-amount, total_fee, current_currency)
        # We use negative amount because heapq is a min-heap, but we want to maximize amount
        pq = [(-amount, 0, source)]

        # Track visited currencies to prevent cycles
        visited = set()

        while pq:
            neg_current_amount, total_fee, current_currency = heapq.heappop(pq)
            current_amount = -neg_current_amount

            # If we reached the destination, return immediately
            # Since we use a max-heap (via negation), this is the best result
            if current_currency == destination:
                return {
                    "total_fee": total_fee,
                    "total_received": current_amount
                }

            # Skip if already visited
            if current_currency in visited:
                continue

            # Mark as visited
            visited.add(current_currency)

            # Explore all outgoing corridors from current currency
            for corridor in self.graph.get(current_currency, []):
                next_currency = corridor["destination"]
                fee = corridor["fee"]
                rate = corridor["rate"]

                # Calculate amount after exchange rate (fee is tracked separately)
                # The fee is deducted from the original amount, not the converted amount
                amount_after_fee = current_amount - fee
                new_amount = amount_after_fee * rate
                new_total_fee = total_fee + fee

                # Only consider this path if the amount is positive and currency not visited
                if new_amount > 0 and next_currency not in visited:
                    heapq.heappush(pq, (-new_amount, new_total_fee, next_currency))

        # No route found from source to destination
        return None


def test_payment_router():
    corridors = [
        ("USD", "EUR", 1.5, 1.2),
        ("EUR", "GBP", 1.0, 0.9),
        ("GBP", "JPY", 2.0, 150.0),
        ("USD", "GBP", 1.2, 0.75),
        ("JPY", "USD", 1.8, 0.0075),
        ("EUR", "USD", 1.5, 1.1),
    ]

    payment_router = PaymentRouter(corridors)

    # Test 1: Simple test case from USD to JPY
    payment_request = {
        "amount": 10000,
        "source_currency": "USD",
        "destination_currency": "JPY",
    }
    result = payment_router.find_best_route(payment_request)
    print(f"Test 1: {result}")
    # Expected: {"total_fee": 4.5, "total_received": 1498500.0}

    # Test 2: Direct USD to EUR without involving other currencies
    payment_request = {
        "amount": 5000,
        "source_currency": "USD",
        "destination_currency": "EUR",
    }
    result = payment_router.find_best_route(payment_request)
    print(f"Test 2: {result}")
    # Expected: {"total_fee": 1.5, "total_received": 6000.0}

    # Test 3: USD to GBP route using one intermediary (USD -> EUR -> GBP)
    payment_request = {
        "amount": 2000,
        "source_currency": "USD",
        "destination_currency": "GBP",
    }
    result = payment_router.find_best_route(payment_request)
    print(f"Test 3: {result}")
    # Expected: {"total_fee": 2.5, "total_received": 1455.0}

    # Test 4: No path available from USD to AUD (unreachable)
    payment_request = {
        "amount": 1000,
        "source_currency": "USD",
        "destination_currency": "AUD",
    }
    result = payment_router.find_best_route(payment_request)
    print(f"Test 4: {result}")
    # Expected: None

    # Test 5: Large amount transaction from EUR to USD with multiple corridors
    payment_request = {
        "amount": 1000000,
        "source_currency": "EUR",
        "destination_currency": "USD",
    }
    result = payment_router.find_best_route(payment_request)
    print(f"Test 5: {result}")
    # Expected: {"total_fee": 1500.0, "total_received": 1100000.0}

    # Test 6: USD to USD should return the original amount with fees
    payment_request = {
        "amount": 500,
        "source_currency": "USD",
        "destination_currency": "USD",
    }
    result = payment_router.find_best_route(payment_request)
    print(f"Test 6: {result}")
    # Expected: {"total_fee": 1.5, "total_received": 498.5}

    print("\nTests completed!")


if __name__ == "__main__":
    test_payment_router()
