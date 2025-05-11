import axios from 'axios';

axios.post('http://localhost:5000/api/register', {
  username: 'user1',
  email: 'test@example.com',
  password: 'secure123'
})
.then(response => {
  console.log(response.data);
})
.catch(error => {
  console.error(error.response.data);
});