# Payment API Reference

Quick reference guide for the Payment API endpoints.

## Base URL
```
/api/v1/payments
```

## Endpoints

### Create Payment Intent
```http
POST /api/v1/payments/intent
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "order_id": "550e8400-e29b-41d4-a716-446655440000",
  "customer_email": "user@example.com"  // optional
}
```

**Success Response (201)**:
```json
{
  "status": "success",
  "data": {
    "payment_id": "660e8400-e29b-41d4-a716-446655440000",
    "client_secret": "pi_xxx_secret_xxx",
    "amount": 1000,
    "currency": "jpy",
    "status": "pending"
  }
}
```

**Error Responses**:
- `400` - Invalid order ID or order status
- `401` - Missing or invalid JWT token
- `403` - Order does not belong to user
- `404` - Order not found

---

### Stripe Webhook Handler
```http
POST /api/v1/payments/webhook
Stripe-Signature: <signature>
Content-Type: application/json

<Stripe webhook payload>
```

**Success Response (200)**:
```json
{
  "status": "success",
  "data": {
    "event_id": "evt_xxx",
    "event_type": "payment_intent.succeeded",
    "payment_intent_id": "pi_xxx",
    "status": "succeeded"
  }
}
```

**Error Response (400)**:
```json
{
  "status": "error",
  "error": "Invalid webhook signature",
  "code": 400
}
```

**Supported Events**:
- `payment_intent.succeeded` - Payment completed successfully
- `payment_intent.payment_failed` - Payment failed
- `payment_intent.canceled` - Payment cancelled

---

### Get Payment Details
```http
GET /api/v1/payments/{payment_id}
Authorization: Bearer <jwt_token>
```

**Success Response (200)**:
```json
{
  "status": "success",
  "data": {
    "id": "660e8400-e29b-41d4-a716-446655440000",
    "order_id": "550e8400-e29b-41d4-a716-446655440000",
    "stripe_payment_intent_id": "pi_xxx",
    "amount": 1000,
    "currency": "jpy",
    "status": "succeeded",
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  }
}
```

**Error Responses**:
- `400` - Invalid payment ID format
- `401` - Missing or invalid JWT token
- `403` - Payment does not belong to user
- `404` - Payment not found

---

## Payment Status Values
- `pending` - Payment intent created, awaiting payment
- `processing` - Payment is being processed
- `succeeded` - Payment completed successfully
- `failed` - Payment failed
- `cancelled` - Payment was cancelled

## Error Response Format
All error responses follow this format:
```json
{
  "status": "error",
  "error": "Error message",
  "code": 400,
  "details": {
    "field": "field_name"
  }
}
```

## Authentication
- All endpoints except `/webhook` require JWT authentication
- Include JWT token in Authorization header: `Bearer <token>`
- Webhook endpoint uses Stripe signature verification instead

## Rate Limiting
- Standard rate limits apply to all endpoints
- Webhook endpoint has higher rate limits for Stripe callbacks

## CORS
- CORS is enabled for configured origins
- Credentials are supported
- Allowed headers: Content-Type, Authorization, X-CSRF-Token

## Security Notes
1. Never expose Stripe secret keys in client-side code
2. Always use HTTPS in production
3. Webhook signature verification is mandatory
4. JWT tokens expire after 1 hour
5. Users can only access their own payment data
