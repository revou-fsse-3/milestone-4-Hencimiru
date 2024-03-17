[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/TId9PLV9)

# BANKING APP
Ini adalah API Banking App, terdapat API untuk users, account dan transactions.

## Postman API URL
https://documenter.getpostman.com/view/32228359/2sA2xnxpTh


## Authentication

Autentikasi yang digunakan adalah bearer token.

## Endpoints

Berikut adalah daftar endpoint yang tersedia beserta deskripsi dan contoh penggunaannya.

### 1. Endpoint Pertama
    /users  
**Deskripsi**: 
    endpoint ini untuk menunjukan semua users yang terdaftar.

**Metode HTTP**: GET

**URL**: `http://127.0.0.1:5000/users/`

**Parameter**:

- `username`
- `password`
- `email`

# RESPON SUKSES
`{
  "users": [
{
      "email": "hencimiru12@gmail.com",
      "id": 1,
      "username": "hencimiru"
    },
    {
      "email": "hencimiru13@gmail.com",
      "id": 5,
      "username": "hencimiru1"
    },

# RESPON ERROR
`{
  "msg": "Missing Authorization Header"
}
