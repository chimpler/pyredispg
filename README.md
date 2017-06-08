```
VERY EARLY VERSION - DO NOT USE
```

PyRedisPg
=========

Redis Server using a Postgres backend.


## TODO

Commands: https://redis.io/commands

Commands			| Status
------------------------------- | :-----:
append				| :x:
auth				| :x:
bgrewriteaof			| :x:
bgsave				| :x:
bitcount			| :x:
bitfield			| :x:
bitop				| :x:
bitpos				| :x:
blpop				| :x:
brpop				| :x:
brpoplpush			| :x:
client kill			| :x:
client list			| :x:
client getname			| :x:
client pause			| :x:
client reply			| :x:
client setname			| :x:
cluster addslots		| :white_check_mark:
cluster count-failure-reports	| :white_check_mark:
cluster countkeysinslot		| :white_check_mark:
cluster delslots		| :white_check_mark:
cluster failover		| :white_check_mark:
cluster forget			| :white_check_mark:
cluster getkeysinslot		| :white_check_mark:
cluster info			| :white_check_mark
cluster keyslot			| :white_check_mark:
cluster meet			| :white_check_mark:
cluster nodes			| :white_check_mark:
cluster replicate		| :white_check_mark:
cluster reset			| :white_check_mark:
cluster saveconfig		| :white_check_mark:
cluster set-config-epoch	| :white_check_mark:
cluster setslot			| :white_check_mark:
cluster slaves			| :white_check_mark:
cluster slots			| :white_check_mark:
command				| :white_check_mark:
command count			| :x:
command getkeys			| :x:
command info			| :x:
config get			| :x:
config rewrite			| :x:
config set			| :x:
config resetstat		| :x:
dbsize				| :white_check_mark:
debug object			| :x:
debug segfault			| :x:
decr				| :x:
decrby				| :x:
del				| :white_check_mark:
discard				| :x:
dump				| :x:
echo				| :white_check_mark:
eval				| :x:
evalsha				| :x:
exec				| :x:
exists				| :white_check_mark:
expire				| :x:
expireat			| :x:
flushall			| :white_check_mark:
flushdb				| :white_check_mark:
geoadd				| :x:
geohash				| :x:
geopos				| :x:
geodist				| :x:
georadius			| :x:
georadiusbymember		| :x:
get				| :white_check_mark:
getbit				| :x:
getrange			| :x:
getset				| :x:
hdel				| :white_check_mark:
hexists				| :white_check_mark:
hget				| :white_check_mark:
hgetall				| :white_check_mark:
hincrby				| :x:
hincrbyfloat			| :x:
hkeys				| :white_check_mark:
hlen				| :white_check_mark:
hmget				| :white_check_mark:
hmset				| :white_check_mark:
hset				| :white_check_mark:
hsetnx				| :x:
hstrlen				| :x:
hvals				| :white_check_mark:
incr				| :x:
incrby				| :x:
incrbyfloat			| :x:
info				| :construction:
keys				| :white_check_mark:
lastsave			| :x:
lindex				| :x:
linsert				| :x:
llen				| :x:
lpop				| :x:
lpush				| :x:
lpushx				| :x:
lrange				| :x:
lrem				| :x:
lset				| :x:
ltrim				| :x:
mget				| :white_check_mark:
migrate				| :x:
monitor				| :x:
move				| :x:
mset				| :x:
msetnx				| :x:
multi				| :x:
object				| :x:
persist				| :white_check_mark:
pexpire				| :x:
pexpireat			| :x:
pfadd				| :x:
pfcount				| :x:
pfmerge				| :x:
ping				| :white_check_mark:
psetex				| :x:
psubscribe			| :x:
pubsub				| :x:
pttl				| :x:
publish				| :x:
punsubscribe			| :x:
quit				| :white_check_mark:
randomkey			| :x:
readonly			| :x:
readwrite			| :x:
rename				| :x:
renamenx			| :x:
restore				| :x:
role				| :x:
rpop				| :x:
rpoplpush			| :x:
rpush				| :x:
rpushx				| :x:
sadd				| :white_check_mark:
save				| :x:
scard				| :white_check_mark:
script debug			| :x:
script exists			| :x:
script flush			| :x:
script kill			| :x:
script load			| :x:
sdiff				| :x:
sdiffstore			| :x:
select				| :white_check_mark:
set				| :construction:
setbit				| :x:
setex				| :x:
setnx				| :x:
setrange			| :x:
shutdown			| :x:
sinter				| :x:
sinterstore			| :x:
sismember			| :x:
slaveof				| :x:
slowlog				| :x:
smembers			| :white_check_mark:
smove				| :x:
sort				| :x:
spop				| :x:
srandmember			| :x:
srem				| :x:
strlen				| :white_check_mark:
subscribe			| :x:
sunion				| :x:
sunionstore			| :x:
swapdb				| :x:
sync				| :x:
time				| :white_check_mark:
touch				| :x:
ttl				| :x:
type				| :white_check_mark:
unsubscribe			| :x:
unlink				| :x:
unwatch				| :x:
wait				| :x:
watch				| :x:
zadd				| :x:
zcard				| :x:
zcount				| :x:
zincrby				| :x:
zinterstore			| :x:
zlexcount			| :x:
zrange				| :x:
zrangebylex			| :x:
zrevrangebylex			| :x:
zrangebyscore			| :x:
zrank				| :x:
zrem				| :x:
zremrangebylex			| :x:
zremrangebyrank			| :x:
zremrangebyscore		| :x:
zrevrange			| :x:
zrevrangebyscore		| :x:
zrevrank			| :x:
zscore				| :x:
zunionstore			| :x:
scan				| :x:
sscan				| :x:
hscan				| :x:
zscan				| :x:

* Improve `command` to return only commands implemented in redis wrapper.
* Use SQL migration tool
