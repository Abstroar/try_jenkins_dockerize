import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import './Register.css';

function Register() {
  const [formData, setFormData] = useState({
    username: "",
    password: "",
    age: "",
    gender: "",
    profile_img: ""
  });
  const [error, setError] = useState("");

  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({...formData, [e.target.name]: e.target.value});
    setError(""); // Clear error when user types
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post("http://127.0.0.1:8000/register", formData);
      navigate("/login");
    } catch (error) {
      setError(error.response?.data?.detail || "Registration failed");
    }
  };

  return (
    <div className="register-container">
      <h2>Register</h2>
      <form className="register-form" onSubmit={handleSubmit}>
        <div className="form-group">
          <input
            name="username"
            placeholder="Username"
            onChange={handleChange}
            value={formData.username}
          />
        </div>
        <div className="form-group">
          <input
            name="password"
            type="password"
            placeholder="Password"
            onChange={handleChange}
            value={formData.password}
          />
        </div>
        <div className="form-group">
          <input
            name="age"
            type="number"
            placeholder="Age"
            onChange={handleChange}
            value={formData.age}
          />
        </div>
        <div className="form-group">
          <input
            name="gender"
            placeholder="Gender"
            onChange={handleChange}
            value={formData.gender}
          />
        </div>
        <div className="form-group">
          <input
            name="profile_img"
            placeholder="Profile Image URL"
            onChange={handleChange}
            value={formData.profile_img}
          />
        </div>
        {error && <div className="error-message">{error}</div>}
        <button className="register-button" type="submit">
          Register
        </button>
      </form>
    </div>
  );
}

export default Register;
