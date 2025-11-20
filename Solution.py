class PaymentRouter:
    def __init__(self, corridors):
        # Initialize with the corridors (to be implemented)
        corridors = self.build_graph(corridors)

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
        # itereate the graph nodes to find the best route
        import heapq

        source = payment_request["source_currency"]
        destination = payment_request["destination_currency"]
        amount = payment_request["amount"]
        graph = self.build_graph(self.corridors)

        # Min-heap priority queue
        pq = [(0, amount, source)]  # (total_fee, current_amount, current_currency)
        visited = {}
        while pq:
            total_fee, current_amount, current_currency = heapq.heappop(pq)

            if current_currency == destination:
                return {"total_fee": total_fee, "total_received": current_amount}

            if current_currency in visited and visited[current_currency] <= total_fee:
                continue
            visited[current_currency] = total_fee

            for corridor in graph.get(current_currency, []):
                next_currency = corridor["destination"]
                fee = corridor["fee"]
                rate = corridor["rate"]

                new_amount = (current_amount - fee) * rate
                new_total_fee = total_fee + fee

                if new_amount > 0:
                    heapq.heappush(pq, (new_total_fee, new_amount, next_currency))
        return None  # No route found


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
    assert result == {
        "total_fee": 4.5,
        "total_received": 1498500.0,
    }, f"Test 1 Failed, Got: {result}"

    # Test 2: Direct USD to EUR without involving other currencies
    payment_request = {
        "amount": 5000,
        "source_currency": "USD",
        "destination_currency": "EUR",
    }
    result = payment_router.find_best_route(payment_request)
    assert result == {
        "total_fee": 1.5,
        "total_received": 6000.0,
    }, f"Test 2 Failed, Got: {result}"

    # Test 3: USD to GBP route using one intermediary (USD -> EUR -> GBP)
    payment_request = {
        "amount": 2000,
        "source_currency": "USD",
        "destination_currency": "GBP",
    }
    result = payment_router.find_best_route(payment_request)
    assert result == {
        "total_fee": 2.5,
        "total_received": 1455.0,
    }, f"Test 3 Failed, Got: {result}"

    # Test 4: No path available from USD to JPY (unreachable)
    payment_request = {
        "amount": 1000,
        "source_currency": "USD",
        "destination_currency": "AUD",  # Assuming no direct or indirect route to AUD
    }
    result = payment_router.find_best_route(payment_request)
    assert result == None, f"Test 4 Failed, Got: {result}"

    # Test 5: Large amount transaction from EUR to USD with multiple corridors
    payment_request = {
        "amount": 1000000,
        "source_currency": "EUR",
        "destination_currency": "USD",
    }
    result = payment_router.find_best_route(payment_request)
    assert result == {
        "total_fee": 1500.0,
        "total_received": 1100000.0,
    }, f"Test 5 Failed, Got: {result}"

    # Test 6: USD to USD should return the original amount with fees
    payment_request = {
        "amount": 500,
        "source_currency": "USD",
        "destination_currency": "USD",
    }
    result = payment_router.find_best_route(payment_request)
    assert result == {
        "total_fee": 1.5,
        "total_received": 498.5,
    }, f"Test 6 Failed, Got: {result}"

    print("All tests passed!")


# Run the tests
test_payment_router()
