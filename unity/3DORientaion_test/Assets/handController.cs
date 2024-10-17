using UnityEngine;

public class handController : MonoBehaviour
{
    private Animator animator;

    private void Awake()
    {
        animator = GetComponent<Animator>();
    }
    // Update is called once per frame
    void Update()
    {
        float grip=0.0f;
        float trigger = 0.0f;

        

         // Check if key 1 is pressed
        if (Input.GetKeyDown(KeyCode.Alpha4))
        {
            Debug.Log("Key 1 pressed");
            grip=1.0f;
            trigger = 0.04f;
            animator.SetFloat("Grip",grip);
            animator.SetFloat("Trigger",trigger);
        }

        // Check if key 2 is pressed
        if (Input.GetKeyDown(KeyCode.Alpha3))
        {
            Debug.Log("Key 2 pressed");
            grip=0.04f;
            trigger = 1.0f;
            animator.SetFloat("Grip",grip);
            animator.SetFloat("Trigger",trigger);
        }

        // Check if key 3 is pressed
        if (Input.GetKeyDown(KeyCode.Alpha2))
        {
            Debug.Log("Key 3 pressed");
            grip=1.0f;
            trigger = 1.0f;
            animator.SetFloat("Grip",grip);
            animator.SetFloat("Trigger",trigger);
        }

        // Check if key 4 is pressed
        if (Input.GetKeyDown(KeyCode.Alpha1))
        {
            Debug.Log("Key 4 pressed");
            grip=0.13f;
            trigger = 0.21f;
            animator.SetFloat("Grip",grip);
            animator.SetFloat("Trigger",trigger);
        }
        

        
    }
}
