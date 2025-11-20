# Problem: Cross-Border Payment Routing Optimization

### Problem Statement:

In a global cryptocurrency exchange platform, you are tasked with optimizing the routing of cross-border payments. Users send and receive cryptocurrency to/from different countries, and the exchange has multiple payment corridors between countries (e.g., the USD to EUR corridor, EUR to JPY corridor). Each corridor has a transaction fee and an associated exchange rate. Some corridors may offer better rates but involve higher fees, while others may be cheaper but slower or have currency conversion delays.

The system must find the most cost-efficient route for a cross-border payment, considering multiple corridors and ensuring that the total fee and conversion rate are optimized.

### Input:

- A list of payment corridors, where each corridor is a tuple of:
    - The source currency (string).
    - The destination currency (string).
    - The fee (float) for the transaction.
    - The exchange rate (float) between the currencies (e.g., USD to EUR might have an exchange rate of 1.2).

    Example:
    ```python
    corridors = [
        ("USD", "EUR", 1.5, 1.2),
        ("EUR", "GBP", 1.0, 0.9),
        ("GBP", "JPY", 2.0, 150.0),
        ("USD", "GBP", 1.2, 0.75),
        ("JPY", "USD", 1.8, 0.0075),
        ("EUR", "USD", 1.5, 1.1)
    ]
    ```

- A payment request consisting of:
    - amount (float) to be sent in the source currency.
    - source currency (string).
    - destination currency (string).

    Example:
    ```python
    payment_request = {
        "amount": 10000,
        "source_currency": "USD",
        "destination_currency": "JPY"
    }
    ```

### Output:

- The most cost-efficient route to complete the payment from the source currency to the destination currency.

- Output the total fee and total amount received after all conversions and fees.

For example, given the payment request above, the system should return the best route (or combination of corridors) for sending 10000 USD to JPY, factoring in fees and exchange rates.

Example Output:
```python
{
    "total_fee": 4.5,
    "total_received": 1498500.0
}
```
