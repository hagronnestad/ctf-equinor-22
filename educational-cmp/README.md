```
$ checksec cmp
[*] '/home/hag/ctf-equinor-22/Educational-cmp/cmp'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```

![](00.png)

![](01.png)

```
$ ./cmp
Enter password to login!
> LEAVEMEALONE
EPT{228dea3beade02d907a77af1c622e18a}
```
