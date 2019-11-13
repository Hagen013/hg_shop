
let baseURL = 'https://torgosvet/api/'

if (process.env.NODE_ENV === 'development') {
  baseURL = 'http://localhost:8000/api/'
}

export default baseURL