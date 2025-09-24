# Foresight

A Python application with a Domain-Driven Design structure.

## Getting Started

### Prerequisites

- Python 3.13 or higher
- [uv](https://github.com/astral-sh/uv) (for package management)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/higorrsc/foresight.git
   ```

2. Navigate to the project directory:

   ```bash
   cd foresight
   ```

3. Create a virtual environment and install dependencies:

   ```bash
   uv venv
   uv pip install -e .[dev]
   ```

### Running the Application

To run the application, execute the following command:

```bash
python main.py
```

## Running Tests

To run the test suite, use the following command:

```bash
pytest
```

## Project Structure

The project follows a Domain-Driven Design (DDD) approach, with the core logic separated into the following layers:

- `src/core/domain`: Contains the core domain models, entities, and value objects.
- `src/core/application`: Contains the application logic and use cases.
- `src/core/infrastructure`: Contains the implementation details, such as repositories and frameworks.
