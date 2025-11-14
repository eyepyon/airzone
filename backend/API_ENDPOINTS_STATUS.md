# API Endpoints Status

## Overview

This document provides a complete overview of all API endpoints in the Airzone backend application, including their implementation status.

## Base URL

All API endpoints are prefixed with: `https://airz.one/api/v1/`

## System Endpoints

### Health Check
- **Endpoint**: `GET /health`
- **Status**: ✓ Implemented
- **Authentication**: None
- **Description**: Service health verification

### API Version
- **Endpoint**: `GET /api/v1`
- **Status**: ✓ Implemented
- **Authentication**: None
- **Description**: API version information and available endpoints

## Authentication Endpoints (Not Implemented)

**Blueprint Status**: ⏳ Not Started (Task 8.2)

- `POST /api/v1/auth/google` - Google OAuth authentication
- `POST /api/v1/auth/refresh` - Token refresh
- `GET /api/v1/auth/me` - Current user information

## NFT Endpoints (Not Implemented)

**Blueprint Status**: ⏳ Not Started (Task 8.3)

- `GET /api/v1/nfts` - User's NFT list
- `POST /api/v1/nfts/mint` - NFT minting request
- `GET /api/v1/nfts/{id}` - NFT details
- `GET /api/v1/nfts/status/{task_id}` - Minting status check

## Product Endpoints (Not Implemented)

**Blueprint Status**: ⏳ Not Started (Task 8.4)

- `GET /api/v1/products` - Product list
- `GET /api/v1/products/{id}` - Product details
- `POST /api/v1/products` - Create product (admin)
- `PUT /api/v1/products/{id}` - Update product (admin)
- `DELETE /api/v1/products/{id}` - Delete product (admin)

## Order Endpoints

**Blueprint Status**: ✓ Implemented (Task 8.5)

### Create Order
- **Endpoint**: `POST /api/v1/orders`
- **Status**: ✓ Implemented
- **Authentication**: JWT Required
- **Request Body**:
  ```json
  {
    "items": [
      {
        "product_id": "uuid",
        "quantity": 1
      }
    ]
  }
  ```
- **Response**: 201 Created
- **Requirements**: 5.1, 5.2, 5.3

### Get User Orders
- **Endpoint**: `GET /api/v1/orders?status=completed&limit=10`
- **Status**: ✓ Implemented
- **Authentication**: JWT Required
- **Query Parameters**:
  - `status` (optional): Filter by order status
  - `limit` (optional): Maximum number of orders (default: 50, max: 100)
- **Response**: 200 OK
- **Requirements**: 5.4

### Get Order Details
- **Endpoint**: `GET /api/v1/orders/{order_id}`
- **Status**: ✓ Implemented
- **Authentication**: JWT Required
- **Response**: 200 OK
- **Requirements**: 5.4

## Payment Endpoints

**Blueprint Status**: ✓ Implemented (Task 8.6)

### Create Payment Intent
- **Endpoint**: `POST /api/v1/payments/intent`
- **Status**: ✓ Implemented
- **Authentication**: JWT Required
- **Request Body**:
  ```json
  {
    "order_id": "uuid",
    "customer_email": "user@example.com"
  }
  ```
- **Response**: 201 Created
- **Requirements**: 5.5

### Stripe Webhook Handler
- **Endpoint**: `POST /api/v1/payments/webhook`
- **Status**: ✓ Implemented
- **Authentication**: Stripe Signature
- **Headers**: `Stripe-Signature`
- **Response**: 200 OK
- **Requirements**: 5.5, 5.6

### Get Payment Details
- **Endpoint**: `GET /api/v1/payments/{payment_id}`
- **Status**: ✓ Implemented
- **Authentication**: JWT Required
- **Response**: 200 OK

## WiFi Session Endpoints

**Blueprint Status**: ✓ Implemented (Task 8.7)

### Create WiFi Session
- **Endpoint**: `POST /api/v1/wifi/connect`
- **Status**: ✓ Implemented
- **Authentication**: None (Captive Portal)
- **Request Body**:
  ```json
  {
    "mac_address": "AA:BB:CC:DD:EE:FF",
    "ip_address": "192.168.1.100",
    "user_id": "uuid"
  }
  ```
- **Response**: 201 Created
- **Requirements**: 2.1, 2.2

### Get WiFi Sessions
- **Endpoint**: `GET /api/v1/wifi/sessions?limit=10`
- **Status**: ✓ Implemented
- **Authentication**: JWT Required
- **Query Parameters**:
  - `limit` (optional): Maximum number of sessions (default: 50, max: 100)
- **Response**: 200 OK
- **Requirements**: 2.4

### Disconnect WiFi Session
- **Endpoint**: `POST /api/v1/wifi/sessions/{session_id}/disconnect`
- **Status**: ✓ Implemented
- **Authentication**: JWT Required
- **Response**: 200 OK
- **Requirements**: 2.3

## Implementation Summary

### Completed Blueprints (3/6)
- ✓ Order Blueprint
- ✓ Payment Blueprint
- ✓ WiFi Blueprint

### Pending Blueprints (3/6)
- ⏳ Auth Blueprint (Task 8.2)
- ⏳ NFT Blueprint (Task 8.3)
- ⏳ Product Blueprint (Task 8.4)

### Total Endpoints
- **Implemented**: 9 endpoints
- **Pending**: 13 endpoints
- **Total**: 22 endpoints

## Error Response Format

All endpoints return errors in the following format:

```json
{
  "status": "error",
  "error": "Error message",
  "code": 400,
  "details": {
    "field": "field_name",
    "message": "Detailed error message"
  }
}
```

## Success Response Format

All endpoints return success responses in the following format:

```json
{
  "status": "success",
  "data": {
    // Response data
  }
}
```

## Authentication

Most endpoints require JWT authentication via the `Authorization` header:

```
Authorization: Bearer <jwt_token>
```

Exceptions:
- Health check endpoint
- API version endpoint
- WiFi connect endpoint (captive portal)
- Stripe webhook endpoint (uses Stripe signature)

## Rate Limiting

Rate limiting is configured in the application to prevent abuse. Limits are applied per IP address.

## CORS Configuration

CORS is configured to allow requests from the frontend application with credentials support.

## Next Steps

1. Implement Auth Blueprint (Task 8.2)
2. Implement NFT Blueprint (Task 8.3)
3. Implement Product Blueprint (Task 8.4)
4. Complete end-to-end testing (Task 9.2)
