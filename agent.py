import torch
import torch.nn as nn
import torch.optim as optim

class MathemagixAgent:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = self.build_model().to(self.device)
        self.optimizer = optim.Adam(self.model.parameters())
        self.criterion = nn.MSELoss()

    def build_model(self):
        input_size = 6 + self.grid_size * self.grid_size  # Adjusted to match the state representation
        hidden_size = 64
        output_size = self.get_action_space_size()

        model = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, output_size)
        )

        return model

    def preprocess_state(self, state):
        player_score, opponent_score, target_score, grid_size, agent_player, turns_taken, hashed_state = state

        # Preprocess hashed_state (2D list)
        preprocessed_hashed_state = torch.tensor(hashed_state, dtype=torch.float32).to(self.device).flatten()

        # Preprocess other elements (regular integers)
        preprocessed_player_score = torch.tensor(player_score, dtype=torch.float32).to(self.device)
        preprocessed_opponent_score = torch.tensor(opponent_score, dtype=torch.float32).to(self.device)
        preprocessed_target_score = torch.tensor(target_score, dtype=torch.float32).to(self.device)
        preprocessed_grid_size = torch.tensor(grid_size, dtype=torch.float32).to(self.device)
        preprocessed_agent_player = torch.tensor(agent_player, dtype=torch.float32).to(self.device)
        preprocessed_turns_taken = torch.tensor(turns_taken, dtype=torch.float32).to(self.device)

        # Concatenate the preprocessed tensors
        preprocessed_state = torch.cat(
            [preprocessed_player_score.unsqueeze(0),
            preprocessed_opponent_score.unsqueeze(0),
            preprocessed_target_score.unsqueeze(0),
            preprocessed_grid_size.unsqueeze(0),
            preprocessed_agent_player.unsqueeze(0),
            preprocessed_turns_taken.unsqueeze(0),
            preprocessed_hashed_state]
        ).requires_grad_()

        return preprocessed_state

    def select_action(self, state):
        with torch.no_grad():
            preprocessed_state = self.preprocess_state(state)
            q_values = self.model(preprocessed_state.unsqueeze(0))
        action = q_values.argmax().item()
        return action

    def update_model(self, state, action, reward, next_state, done):
        preprocessed_state = self.preprocess_state(state)
        preprocessed_next_state = self.preprocess_state(next_state)

        with torch.no_grad():
            target = reward
            if not done:
                next_q_values = self.model(preprocessed_next_state.unsqueeze(0))
                max_next_q_value = next_q_values.max().item()
                target += max_next_q_value

            q_values = self.model(preprocessed_state.unsqueeze(0))
            target_q = q_values.clone()
            target_q[0][action] = target

        self.optimizer.zero_grad()
        loss = self.criterion(q_values, target_q)
        loss.backward()
        self.optimizer.step()

    def get_action_space_size(self):
        action_space_size = 4 + 4 * self.grid_size * self.grid_size
        return action_space_size
