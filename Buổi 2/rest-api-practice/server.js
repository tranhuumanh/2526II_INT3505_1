const express = require("express");
const app = express();

app.use(express.json());

// Fake database
let users = [
  { id: 1, name: "Manh Tran", email: "manh@gmail.com" },
  { id: 2, name: "Nguyen Van A", email: "a@gmail.com" }
];

// 1. GET - Lấy danh sách user
app.get("/users", (req, res) => {
  res.status(200).json(users);
});

// 2. GET - Lấy user theo ID
app.get("/users/:id", (req, res) => {
  const id = parseInt(req.params.id);

  const user = users.find(u => u.id === id);

  if (!user) {
    return res.status(404).json({ error: "User not found" });
  }

  res.status(200).json(user);
});

// 3. POST - Tạo user mới
app.post("/users", (req, res) => {

  const newUser = {
    id: users.length + 1,
    name: req.body.name,
    email: req.body.email
  };

  users.push(newUser);

  res.status(201).json(newUser);
});
//  PUT - Update toàn bộ user
app.put("/users/:id", (req, res) => {

  const id = parseInt(req.params.id);

  const user = users.find(u => u.id === id);

  if (!user) {
    return res.status(404).json({ error: "User not found" });
  }

  user.name = req.body.name;
  user.email = req.body.email;

  res.status(200).json(user);
});

// 4. PATCH - Update email
app.patch("/users/:id", (req, res) => {

  const id = parseInt(req.params.id);

  const user = users.find(u => u.id === id);

  if (!user) {
    return res.status(404).json({ error: "User not found" });
  }

  user.email = req.body.email;

  res.status(200).json(user);
});

// 5. DELETE - Xóa user
app.delete("/users/:id", (req, res) => {

  const id = parseInt(req.params.id);

  const index = users.findIndex(u => u.id === id);

  if (index === -1) {
    return res.status(404).json({ error: "User not found" });
  }

  users.splice(index, 1);

  res.status(204).send();
});
