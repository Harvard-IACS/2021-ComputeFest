from itertools import chain
import torch
import torch.nn.functional as F

device ="cpu"
SPECIAL_TOKENS = ["<bos>", "<eos>", "<speaker1>", "<speaker2>", "<pad>"]
ATTR_TO_SPECIAL_TOKEN = {
    "bos_token": "<bos>",
    "eos_token": "<eos>",
    "pad_token": "<pad>",
    "additional_special_tokens": ["<speaker1>", "<speaker2>"],
}
MODEL_INPUTS = ["input_ids", "mc_token_ids", "lm_labels", "mc_labels", "token_type_ids"]
PADDED_INPUTS = ["input_ids", "lm_labels", "token_type_ids"]

def build_input_from_segments(persona, history, reply, tokenizer, lm_labels=False, with_eos=True):
  """ Build a sequence of input from 3 segments: persona, history and last reply. """
  bos, eos, speaker1, speaker2 = tokenizer.convert_tokens_to_ids(SPECIAL_TOKENS[:-1])
  sequence = [[bos] + list(chain(*persona))] + history + [reply + ([eos] if with_eos else [])]
  sequence = [sequence[0]] + [
      [speaker2 if (len(sequence) - i) % 2 else speaker1] + s for i, s in enumerate(sequence[1:])
  ]
  instance = {}
  instance["input_ids"] = list(chain(*sequence))
  instance["token_type_ids"] = [speaker2 if i % 2 else speaker1 for i, s in enumerate(sequence) for _ in s]
  instance["mc_token_ids"] = len(instance["input_ids"]) - 1
  instance["lm_labels"] = [-100] * len(instance["input_ids"])
  if lm_labels:
      instance["lm_labels"] = ([-100] * sum(len(s) for s in sequence[:-1])) + [-100] + sequence[-1][1:]
  return instance

def top_filtering(logits, top_k=0.0, top_p=0.9, threshold=-float("Inf"), filter_value=-float("Inf")):
  top_k = min(top_k, logits.size(-1))
  if top_k > 0:
      # Remove all tokens with a probability less than the last token in the top-k tokens
      indices_to_remove = logits < torch.topk(logits, top_k)[0][..., -1, None]
      logits[indices_to_remove] = filter_value

  if top_p > 0.0:
      # Compute cumulative probabilities of sorted tokens
      sorted_logits, sorted_indices = torch.sort(logits, descending=True)
      cumulative_probabilities = torch.cumsum(F.softmax(sorted_logits, dim=-1), dim=-1)

      # Remove tokens with cumulative probability above the threshold
      sorted_indices_to_remove = cumulative_probabilities > top_p
      # Shift the indices to the right to keep also the first token above the threshold
      sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()
      sorted_indices_to_remove[..., 0] = 0

      # Back to unsorted indices and set them to -infinity
      indices_to_remove = sorted_indices[sorted_indices_to_remove]
      logits[indices_to_remove] = filter_value

  indices_to_remove = logits < threshold
  logits[indices_to_remove] = filter_value

  return logits

def sample_sequence(personality, history, tokenizer, model, current_output=None):

  special_tokens_ids = tokenizer.convert_tokens_to_ids(SPECIAL_TOKENS)
  if current_output is None:
      current_output = []

  # Args
  max_length = 20
  temperature = 0.7
  top_k = 0
  top_p = 0.90
  do_sample = True
  min_length = 1


  for i in range(max_length):
      instance = build_input_from_segments(
          personality, history, current_output, tokenizer, with_eos=False
      )

      input_ids = torch.tensor(instance["input_ids"], device=device).unsqueeze(0)
      token_type_ids = torch.tensor(instance["token_type_ids"], device=device).unsqueeze(0)

      logits = model(input_ids, token_type_ids=token_type_ids)
      logits = logits[0]

      logits = logits[0, -1, :] / temperature
      logits = top_filtering(logits, top_k=top_k, top_p=top_p)
      probs = F.softmax(logits, dim=-1)

      prev = torch.topk(probs, 1)[1] if not do_sample else torch.multinomial(probs, 1)
      if i < min_length and prev.item() in special_tokens_ids:
          while prev.item() in special_tokens_ids:
              if probs.max().item() == 1:
                  break  # avoid infinitely looping
              prev = torch.multinomial(probs, num_samples=1)

      if prev.item() in special_tokens_ids:
          break
      current_output.append(prev.item())

  return current_output