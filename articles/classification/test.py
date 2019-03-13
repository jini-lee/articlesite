import tensorflow as tf
import os
import sys 
import argparse


def main(unused_argv):
  # Give a folder path as an argument with '--log_dir' to save
  # TensorBoard summaries. Default is a log folder in current directory.
  current_path = os.path.dirname(os.path.realpath(sys.argv[0]))

  parser = argparse.ArgumentParser()
  parser.add_argument(
      '--log_dir',
      type=str,
      default=os.path.join(current_path, 'log'),
      help='The log directory for TensorBoard summaries.')
  flags, unused_flags = parser.parse_known_args()
  print(flags.args.--log_dir)

if __name__ == '__main__':
  tf.app.run()
