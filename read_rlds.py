
import tensorflow_datasets as tfds

import tqdm
import numpy as np
import cv2
import time
import argparse
import matplotlib.pyplot as plt

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--rlds_dir", type=str, default="test_log2")
    parser.add_argument("--show_img", action="store_true")
    parser.add_argument("--show_figures", action="store_true", help="show images in matplotlib")
    parser.add_argument("--replay", action="store_true", help="replay the trajectory on gym env")
    parser.add_argument("--ip", type=str, default="ip if we are replaying")
    args = parser.parse_args()

    ds_builder = tfds.builder_from_directory(args.rlds_dir)
    dataset = ds_builder.as_dataset(split='all')
    
    if args.replay:
        from manipulator_gym.manipulator_env import ManipulatorEnv
        from manipulator_gym.interfaces.interface_service import ActionClientInterface
        env = ManipulatorEnv(manipulator_interface=ActionClientInterface(host=args.ip))

    # print len of dataset
    # print("size of dataset", len(list(dataset)))
    # assert len(list(dataset)) == num_of_episodes, f"There should be 3 episodes in the dataset"
    # dataset = dataset.repeat().shuffle(1).batch(1)
    dataset = dataset.take(1).cache().repeat()
    it = iter(dataset)

    for i in tqdm.tqdm(range(3)):
        episode = next(it)
        print("key in a traj: ", episode.keys())

        steps = episode['steps']
        prim_img_buffer = []
        wrist_img_buffer = []
        
        if args.replay:
            env.reset()
        
        for step in steps:
            print(step['observation'].keys())
            # print(" - state: ", step['observation']['state'])

            if args.show_img:
                img = step['observation']['image_primary']
                img = np.array(img)
                cv2.imshow("img", img)
                cv2.waitKey(10)

            if args.show_figures:
                prim_img_buffer.append(step['observation']['image_primary'])
                wrist_img_buffer.append(step['observation']['image_wrist'])
            
            if args.show_figures and len(prim_img_buffer) == 10:
                # show both images in matplot lib with 2 rows and 10 columns
                fig, axs = plt.subplots(2, 10)
                for i in range(10):
                    axs[0, i].imshow(prim_img_buffer[i])
                    axs[1, i].imshow(wrist_img_buffer[i])
                plt.show()
                prim_img_buffer = []
                wrist_img_buffer = []
                
            if args.replay:
                action = step['action']
                print("replaying action: ", action)
                done = env.step(action)
                time.sleep(0.1)

    print("done")
    del it, dataset
    cv2.destroyAllWindows()
