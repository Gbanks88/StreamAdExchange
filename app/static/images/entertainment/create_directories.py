import os

# Create directories for different image categories
directories = [
    'streams',
    'games',
    'sports',
    'avatars',
    'services',
    'promos'
]

base_path = os.path.dirname(os.path.abspath(__file__))

for directory in directories:
    path = os.path.join(base_path, directory)
    if not os.path.exists(path):
        os.makedirs(path) 